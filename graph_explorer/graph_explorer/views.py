from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.apps import apps
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
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

def apply_filter(request, workspace_id):
    if request.method == "POST":
        #current_workspace = get_current_workspace(request, workspace_id)
        #graph = current_workspace["current_graph"]

        #graph = get_current_graph(request) # for now this one, we need to use the graph from the currently active workspace

        filters = {
            "attribute_name": request.POST.get("filter_attribute_name"),
            "comparator": request.POST.get("filter_comparator"),
            "attribute_value": request.POST.get("filter_attribute_value"),
            "search": request.POST.get("filter_search"),
        }

        # apply filters to the graph
        try:
            pass
            #graph = graph.apply_filters(filters)
            #print(graph)
            # update filters and filtered graph (G1 -> G2) from the current workspace
            #current_workspace["filters"].append(filters)
            #current_workspace["current_graph"] = graph
        except ValueError:
            return HttpResponseBadRequest("Invalid filter.")

    # so the new filtered graph can be reloaded on the current workspace
    return redirect("index", workspace_id=workspace_id)

def reset_filters(request, workspace_id):
    """
    current_workspace = get_workspace_state(request, workspace_id)
    current_workspace["current_graph"] = current_workspace["original_graph"]
    current_workspace["filters"] = []
    """

    return redirect("index", workspace_id=workspace_id)
