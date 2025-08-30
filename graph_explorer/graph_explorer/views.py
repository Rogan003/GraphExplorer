import pkg_resources
from django.shortcuts import render, redirect
from django.apps import apps
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP, DATA_SOURCE_LOADERS_GROUP
from use_cases.workspace.workspace_service import (
    handle_initial_workspace,
    upload_file,
    get_active_workspace,
    create_workspace,
    get_config_for_workspace
)

def index(request):
    # request.session.flush()
    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    workspaces = handle_initial_workspace(request.session, plugin_service, tree_view_service)

    path = upload_file(request)

    if path is None and request.method == "POST" and request.POST.get("url"):
        path = request.POST.get("url")

    active_ws_id = int(request.GET.get("tab", len(workspaces)))
    new_ws_flag = request.GET.get("new_workspace") == "true"

    data_source_config = None

    if request.method == "GET" and request.GET.get("is_graph_directed") and request.GET.get("reference_attribute") \
            and request.GET.get("loader_type"):
        data_source_config = {
            "is_graph_directed": request.GET.get("is_graph_directed") == "true",
            "reference_attribute": request.GET.get("reference_attribute"),
            "loader_type": request.GET.get("loader_type"),
        }

    if new_ws_flag:
        active_workspace, workspaces = create_workspace(
            request.session,
            path=path,
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
            path=path,
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
        "workspace_count": len(workspaces),
        "loader_type": active_workspace.configuration.loader_type.identifier() if active_workspace else None
    })

def data_source_config(request, ws_id):
    if request.method == "POST" and request.POST.get("is_graph_directed") and request.POST.get("reference_attribute")\
            and request.POST.get("loader_type"):

        return redirect(f"/?tab={ws_id}&is_graph_directed={request.POST.get('is_graph_directed')}&reference_attribute={request.POST.get('reference_attribute')}&loader_type={request.POST.get('loader_type')}")

    loaders = pkg_resources.iter_entry_points(group=DATA_SOURCE_LOADERS_GROUP)
    return render(request, "data_source_configuration.html", {
        "loaders" : loaders,
        "active_workspace_id": ws_id,
        "config" : get_config_for_workspace(request.session, ws_id)
    })