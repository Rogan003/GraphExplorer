from django.shortcuts import render, redirect
from django.apps import apps
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.workspace.workspace_service import (
    handle_initial_workspace,
    upload_file,
    get_active_workspace,
    create_workspace,
    update_workspace_in_session,
)

from use_cases.filter.filter import Filter


def index(request):
    # request.session.flush()
    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    workspaces = handle_initial_workspace(request.session, plugin_service, tree_view_service)

    file_path = upload_file(request)

    active_ws_id = int(request.GET.get("tab", len(workspaces)))
    new_ws_flag = request.GET.get("new_workspace") == "true"

    if new_ws_flag:
        active_workspace, workspaces = create_workspace(
            request.session,
            file_path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
        )
    else:
        active_workspace, workspaces = get_active_workspace(
            request.session,
            active_ws_id,
            file_path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
        )

    if request.GET.get("reset_filters"):
        return reset_filters(request, active_workspace)
    else:
        filter_error_msg = apply_filters(request, active_workspace)

    if active_workspace and filter_error_msg is None:
        active_workspace.load_graph(plugin_service, tree_view_service)

    return render(request, "index.html", {
        "visualizer_plugins": plugin_service.plugins[VISUALIZER_GROUP],
        "data_source_plugins": plugin_service.plugins[DATA_SOURCE_GROUP],
        "graph_html": active_workspace.graph_html if active_workspace else "No graph yet",
        "selected_visualizer_identifier": active_workspace.visualizer_identifier if active_workspace else None,
        "selected_data_source_identifier": active_workspace.data_source_identifier if active_workspace else None,
        "tree_view": active_workspace.tree_view if active_workspace else None,
        "workspaces": workspaces,
        "active_workspace_id": active_ws_id,
        "filter_error_msg": filter_error_msg,
    })

def apply_filters(request, ws):
    filter_error_msg = None

    if ws is not None:
        filters = Filter (
            request.POST.get("filter_attribute_name"),
            request.POST.get("filter_comparator"),
            request.POST.get("filter_attribute_value"),
            request.POST.get("filter_search"),
        )

        try:
            ws.add_filter(filters)
            update_workspace_in_session(request.session, ws)

        except ValueError:
            filter_error_msg = "Invalid filter."

    return filter_error_msg

def reset_filters(request, ws):
    if ws is not None:
        ws.clear_filters()
        update_workspace_in_session(request.session, ws)

    query_params = request.GET.copy()
    while "reset_filters" in query_params:
        query_params.pop("reset_filters", None)

    url = request.path

    if query_params:
        url += "?" + query_params.urlencode()

    return redirect(url)
