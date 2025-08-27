import pkg_resources
from django.shortcuts import render
from django.apps import apps
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP, DATA_SOURCE_LOADERS_GROUP
from use_cases.workspace.workspace_service import (
    handle_initial_workspace,
    upload_file,
    get_active_workspace,
    create_workspace,
)

def index(request):
    # request.session.flush()
    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    workspaces = handle_initial_workspace(request.session, plugin_service, tree_view_service)

    file_path = upload_file(request)

    active_ws_id = int(request.GET.get("tab", len(workspaces)))
    new_ws_flag = request.GET.get("new_workspace") == "true"

    data_source_config = None

    if request.method == "POST" and request.POST.get("graph_type") and request.POST.get("reference_attribute") \
            and request.POST.get("loader_type"):
        data_source_config = {
            "graph_type": request.POST.get("graph_type"),
            "reference_attribute": request.POST.get("reference_attribute"),
            "loader_type": request.POST.get("loader_type"),
        }

    if new_ws_flag:
        active_workspace, workspaces = create_workspace(
            request.session,
            path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
            data_source_config=data_source_config
        )
    else:
        active_workspace, workspaces = get_active_workspace(
            request.session,
            active_ws_id,
            path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
            data_source_config=data_source_config
        )

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

def data_source_config(request):
    if request.method == "POST" and request.POST.get("graph_type") and request.POST.get("reference_attribute")\
            and request.POST.get("loader_type"):
        return index(request)

    loaders = pkg_resources.iter_entry_points(group=DATA_SOURCE_LOADERS_GROUP)
    return render(request, "data_source_configuration.html", {
        "loaders" : loaders
    })