import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zolits_backend.settings')
django.setup()

from core.models import System, Module, Submodule

def seed_normalization():
    data = [
        {
            "system": "ZUMS",
            "modules": [
                {
                    "name": "CRM",
                    "submodules": [
                        "security deposit review", "Se enrollment", "fraud management", 
                        "planned outage", "customer material purchase", "new connection", 
                        "fault outage", "annual budget", "change tariff", 
                        "net metering connection", "budget adjustment", "standard connection", 
                        "basic info change test 1", "ownership transfer", 
                        "temporary connection", "change capacity", "budget management"
                    ]
                }
            ]
        },
        {
            "system": "Assets",
            "modules": [
                {
                    "name": "Assets",
                    "submodules": ["inbound delivery", "outbound delivery", "scrap management"]
                }
            ]
        },
        {
            "system": "NDPM",
            "modules": [
                {
                    "name": "NDPM",
                    "submodules": ["overtime", "internal project"]
                }
            ]
        }
    ]

    for sys_data in data:
        system, _ = System.objects.get_or_create(name=sys_data["system"])
        for mod_data in sys_data["modules"]:
            module, _ = Module.objects.get_or_create(system=system, name=mod_data["name"])
            for sub_name in mod_data["submodules"]:
                Submodule.objects.get_or_create(module=module, name=sub_name)

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_normalization()
