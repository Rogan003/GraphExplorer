from django.http import HttpResponseBadRequest
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

    """
    f = Filter(attribute_name="name", comparator="contains", attribute_value=None, search_value="Alice")
    ws.add_filter(f)
    
    request.session["workspace"] = ws.to_dict()
    saved = request.session["workspace"]
    ws = Workspace.from_dict(saved)
    """

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

def apply_filter(request):
    filter_error_msg= None

    if request.method == "POST":
        ws_id = request.POST.get("active_workspace_id") or request.GET.get("tab")

        if ws_id is None:
            filter_error_msg = "No workspace ID provided."
        else:
            ws_id = int(ws_id)
            ws, _ = get_active_workspace(request.session, ws_id)
            if not ws:
                filter_error_msg = "Workspace not found."
            else:
                filters = {
                    "attribute_name": request.POST.get("filter_attribute_name"),
                    "comparator": request.POST.get("filter_comparator"),
                    "attribute_value": request.POST.get("filter_attribute_value"),
                    "search": request.POST.get("filter_search"),
                }

                try:
                    ws.add_filter(filters)
                    plugin_service = apps.get_app_config("graph_explorer").plugin_service
                    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service
                    ws.load_graph(plugin_service, tree_view_service)
                    update_workspace_in_session(request.session, ws)
                except ValueError:
                    filter_error_msg = "Invalid filter."

        plugin_service = apps.get_app_config("graph_explorer").plugin_service
        tree_view_service = apps.get_app_config("graph_explorer").tree_view_service
        workspaces = handle_initial_workspace(request.session, plugin_service, tree_view_service)
        active_workspace, _ = get_active_workspace(request.session, ws_id or 0)

        return render(request, "index.html", {
            "visualizer_plugins": plugin_service.plugins[VISUALIZER_GROUP],
            "data_source_plugins": plugin_service.plugins[DATA_SOURCE_GROUP],
            "graph_html": active_workspace.graph_html if active_workspace else "No graph yet",
            "selected_visualizer_identifier": active_workspace.visualizer_identifier if active_workspace else None,
            "selected_data_source_identifier": active_workspace.data_source_identifier if active_workspace else None,
            "tree_view": active_workspace.tree_view if active_workspace else None,
            "workspaces": workspaces,
            "active_workspace_id": ws_id or 0,
            "filter_error_msg": filter_error_msg,
        })

    return HttpResponseBadRequest("Error")


def reset_filters(request):
    ws_id = request.POST.get("workspace_id") or request.GET.get("tab")
    if ws_id is None:
        return HttpResponseBadRequest("No workspace ID provided.")
    ws_id = int(ws_id)

    ws, _ = get_active_workspace(request.session, ws_id)
    if not ws:
        return HttpResponseBadRequest("Workspace not found.")

    ws.clear_filters()

    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service
    ws.load_graph(plugin_service, tree_view_service)

    update_workspace_in_session(request.session, ws)

    return redirect("index", tab=ws_id)
