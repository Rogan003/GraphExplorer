from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.apps import apps
from use_cases.workspace import Workspace
from use_cases.workspace_manager import get_workspaces, add_workspace
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP

def index(request):
    # request.session.flush()
    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    workspaces = get_workspaces(request.session)
    if not workspaces:
        ws = Workspace(
            id=0,
            file_path=None,
            data_source_identifier=None,
            visualizer_identifier=None,
        )
        ws.load_graph(plugin_service, tree_view_service)
        add_workspace(request.session, ws)
        workspaces = get_workspaces(request.session)

    new_ws = request.GET.get("new_workspace")
    active_ws_id = int(request.GET.get("tab", len(workspaces)-1)) if workspaces else 0

    file_path = None
    if request.method == "POST" and request.FILES.get("file"):
        fs = FileSystemStorage()
        filename = fs.save(request.FILES["file"].name, request.FILES["file"])
        file_path = fs.path(filename)

        if workspaces and 0 <= active_ws_id < len(workspaces):
            ws_dict = workspaces[active_ws_id]
            ws = Workspace(**ws_dict)
            ws.file_path = file_path
            ws.load_graph(plugin_service, tree_view_service)
            active_workspace = ws

            workspaces[active_ws_id] = ws.to_dict()
            request.session["workspaces"] = workspaces
        else:
            new_ws = True


    if new_ws == "true":
        ws = Workspace(
            id=len(workspaces),
            file_path=file_path,
            data_source_identifier=request.GET.get("datasource"),
            visualizer_identifier=request.GET.get("visualizer"),
        )
        ws.load_graph(plugin_service, tree_view_service)
        add_workspace(request.session, ws)
        active_ws_id = ws.id
        workspaces = get_workspaces(request.session) 

    active_workspace = None
    if workspaces and 0 <= active_ws_id < len(workspaces):
        ws_dict = workspaces[active_ws_id]
        ws = Workspace(**ws_dict)

        if request.GET.get("visualizer"):
            ws.visualizer_identifier = request.GET.get("visualizer")
        if request.GET.get("datasource"):
            ws.data_source_identifier = request.GET.get("datasource")
        if file_path:
            ws.file_path = file_path

        ws.load_graph(plugin_service, tree_view_service)
        active_workspace = ws

        workspaces[active_ws_id] = ws.to_dict()
        request.session["workspaces"] = workspaces


    return render(request, "index.html", {
        "visualizer_plugins": plugin_service.plugins[VISUALIZER_GROUP],
        "data_source_plugins": plugin_service.plugins[DATA_SOURCE_GROUP],
        "graph_html": active_workspace.graph_html if active_workspace else "No graph yet",
        "selected_visualizer_identifier": active_workspace.visualizer_identifier if active_workspace else None,
        "selected_data_source_identifier": active_workspace.data_source_identifier if active_workspace else None,
        "tree_view": active_workspace.tree_view if active_workspace else None,
        "workspaces": workspaces,
        "active_workspace_id": active_ws_id,
    })
