import { Component, HostListener, Injectable, ViewChild } from "@angular/core";
import { BehaviorSubject, Observable, Subscription } from "rxjs";
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
} from "@angular/material/tree";
import { FlatTreeControl } from "@angular/cdk/tree";
import { SidebarService } from "src/app/services/sidebar.service";
import { Router } from "@angular/router";
import { MatInput } from "@angular/material/input";

interface FileNode {
  name: string;
  children?: FileNode[];
  route?: string;
  icon?: string;
}

interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
  route?: string;
  icon?: string;
}

@Component({
  selector: "app-sidebar",
  templateUrl: "./sidebar.component.html",
  styleUrls: ["./sidebar.component.scss"],
})
export class SidebarComponent {
  public sidebarMode: any = "side";
  sidebarVisible = false;
  private subscription: Subscription;
  searchQuery: string = "";

  treeControl: FlatTreeControl<FlatNode>;
  treeFlattener: MatTreeFlattener<FileNode, FlatNode>;
  dataSource: MatTreeFlatDataSource<FileNode, FlatNode>;
  TREE_DATA: FileNode[] = [];

  constructor(private sidebarService: SidebarService, private router: Router) {
    this.subscription = this.sidebarService.sidebarVisible.subscribe(
      (visible) => (this.sidebarVisible = visible)
    );

    // Initialize the tree flattener
    this.treeFlattener = new MatTreeFlattener<FileNode, FlatNode>(
      (node: FileNode, level: number) => ({
        expandable: !!node.children,
        name: node.name,
        level: level,
        route: node.route,
        icon: node.icon,
      }),
      (node) => node.level,
      (node) => node.expandable,
      (node) => node.children
    );

    this.treeControl = new FlatTreeControl<FlatNode>(
      (node) => node.level,
      (node) => node.expandable
    );

    this.dataSource = new MatTreeFlatDataSource(
      this.treeControl,
      this.treeFlattener
    );

    // Load your data into the dataSource
    this.loadData();
  }

  hasChild = (_: number, node: FlatNode) => node.expandable;

  loadData() {
    // You would fetch the tree data from the service and load it here
    // For example, this.sidebarService.getTreeData().subscribe(data => this.dataSource.data = data);
    // Hardcoded data for demonstration
    this.TREE_DATA = [
      {
        name: "Dashboard",
        route: "/dashboard",
        icon: "dashboard",
      },
      {
        name: "Documents",
        children: [
          { name: "Invoices", route: "/dashboard/invoices" },
          { name: "Invoice Proformas", route: "/dashboard/invoice-proformas" },
          { name: "Invoice Stornos", route: "/dashboard/invoice-stornos" },
        ],
        icon: "description",
      },
      {
        name: "Inventory",
        children: [
          { name: "Clients", route: "/dashboard/clients" },
          { name: "Products", route: "/dashboard/products" },
        ],
        icon: "inventory",
      },
      {
        name: "Settings",
        children: [
          { name: "Firm Details", route: "/dashboard/firm-details" },
          { name: "Bank Accounts", route: "/dashboard/bank-accounts" },
          { name: "Document Series", route: "/dashboard/document-series" },
        ],
        icon: "settings",
      },
    ];

    this.dataSource.data = this.TREE_DATA;
    this.treeControl.expandAll();
  }

  // Implement a search/filter function
  filterTree(event: Event) {
    const target = event.target as HTMLInputElement;
    const filterText = target.value.trim().toLowerCase();

    if (!filterText) {
      this.loadData(); // Reset the tree when there's no filter
      this.treeControl.collapseAll(); // Optionally collapse all if resetting
    } else {
      // Filter the tree based on the input
      this.dataSource.data = this.filterNodes(this.TREE_DATA, filterText);
      this.treeControl.expandAll(); // Expand all for simplicity in showing filtered results
    }
  }

  // Recursive function to filter nodes based on the search text
  filterNodes(nodes: any[], searchText: string): any[] {
    return nodes.reduce((filtered: any[], node) => {
      // Clone the node to avoid mutating the original data
      const filteredNode = Object.assign({}, node);

      // If the node has children, recursively filter them
      if (node.children) {
        filteredNode.children = this.filterNodes(node.children, searchText);
      }

      // Determine if the current node or any of its filtered children match the search text
      if (
        node.name.toLowerCase().includes(searchText) ||
        (filteredNode.children && filteredNode.children.length > 0)
      ) {
        filtered.push(filteredNode);
      }

      return filtered;
    }, []);
  }

  toggleNode(node: any): void {
    this.treeControl.isExpanded(node)
      ? this.treeControl.collapse(node)
      : this.treeControl.expand(node);
  }

  isActiveRoute(nodeRoute: string): boolean {
    return this.router.url === nodeRoute;
  }

  clearSearch() {
    this.searchQuery = "";
    this.filterTree({ target: { value: "" } } as any);
    this.treeControl.expandAll();
  }

  closeSidebar() {
    if (window.innerWidth < 1500) {
      this.sidebarService.toggleSidebar();
    }
  }
}
