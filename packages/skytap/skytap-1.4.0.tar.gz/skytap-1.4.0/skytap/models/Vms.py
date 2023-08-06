"""Support for Skytap VMs."""
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vm import Vm


class Vms(SkytapGroup):
    """A list of VMs."""

    def __init__(self, vms_json, env_url):
        """Create the list of VMs.

        Args:
            vms_json (string): The JSON from Skytap API to build the list from.
            parent (Environment or Template): The parent object -
                                              environment or template.

        """
        super(Vms, self).__init__()
        self.load_list_from_json(vms_json, Vm, env_url)
        for each_vm in self.data:
            self.data[each_vm].data['url'] = (env_url + '/vms/'
                                              "" + str(self.data[each_vm].id))
