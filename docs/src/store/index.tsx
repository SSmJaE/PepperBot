import { proxy, useSnapshot } from "valtio";

export const capabilityTypes = ["command", "handler", "product"] as const;
export type CapabilityType = typeof capabilityTypes[number];

export const packageManagers = ["pip", "poetry", "pdm"] as const;
export type PackageManagerType = typeof packageManagers[number];

class Store {
    selectedTypes: CapabilityType[] = [...capabilityTypes];
    toggleSelectedType(type: CapabilityType) {
        if (this.selectedTypes.includes(type)) {
            this.selectedTypes = this.selectedTypes.filter((t) => t !== type);
        } else {
            this.selectedTypes = [...this.selectedTypes, type];
        }
    }

    packageManager: PackageManagerType = "pdm";
    setPackageManager(manager: PackageManagerType) {
        this.packageManager = manager;
    }
}

export const store = proxy(new Store());

export const useStore = () => useSnapshot(store);
