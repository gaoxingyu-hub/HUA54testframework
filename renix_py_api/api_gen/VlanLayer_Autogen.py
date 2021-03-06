"""
Auto-generated File 
Create Time: 2019-12-27 02:33:26
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .NetworkLayer_Autogen import NetworkLayer


@rom_manager.rom
class VlanLayer(NetworkLayer):
    def __init__(self, VlanId=None, Step=None, VlanIdList=None, Priority=None, PriorityStep=None, PriorityList=None, Cfi=None, Tpid=None, **kwargs):
        self._VlanId = VlanId  # VLAN ID
        self._Step = Step  # VLAN ID Step
        self._VlanIdList = VlanIdList  # VLAN ID List
        self._Priority = Priority  # VLAN Priority
        self._PriorityStep = PriorityStep  # VLAN Priority Step
        self._PriorityList = PriorityList  # VLAN Priority List
        self._Cfi = Cfi  # CFI
        self._Tpid = Tpid  # TPID

        properties = kwargs.copy()
        if VlanId is not None:
            properties['VlanId'] = VlanId
        if Step is not None:
            properties['Step'] = Step
        if VlanIdList is not None:
            properties['VlanIdList'] = VlanIdList
        if Priority is not None:
            properties['Priority'] = Priority
        if PriorityStep is not None:
            properties['PriorityStep'] = PriorityStep
        if PriorityList is not None:
            properties['PriorityList'] = PriorityList
        if Cfi is not None:
            properties['Cfi'] = Cfi
        if Tpid is not None:
            properties['Tpid'] = Tpid

        # call base class function, and it will send message to renix server to create a class.
        super(VlanLayer, self).__init__(**properties)

    def delete(self):
        """
        call to delete itself
        """
        return self._finalize()

    def edit(self, VlanId=None, Step=None, VlanIdList=None, Priority=None, PriorityStep=None, PriorityList=None, Cfi=None, Tpid=None, **kwargs):
        properties = kwargs.copy()
        if VlanId is not None:
            self._VlanId = VlanId
            properties['VlanId'] = VlanId
        if Step is not None:
            self._Step = Step
            properties['Step'] = Step
        if VlanIdList is not None:
            self._VlanIdList = VlanIdList
            properties['VlanIdList'] = VlanIdList
        if Priority is not None:
            self._Priority = Priority
            properties['Priority'] = Priority
        if PriorityStep is not None:
            self._PriorityStep = PriorityStep
            properties['PriorityStep'] = PriorityStep
        if PriorityList is not None:
            self._PriorityList = PriorityList
            properties['PriorityList'] = PriorityList
        if Cfi is not None:
            self._Cfi = Cfi
            properties['Cfi'] = Cfi
        if Tpid is not None:
            self._Tpid = Tpid
            properties['Tpid'] = Tpid

        super(VlanLayer, self).edit(**properties)

    @property
    def VlanId(self):
        """
        get the value of property _VlanId
        """
        if self.force_auto_sync:
            self.get('VlanId')
        return self._VlanId

    @property
    def Step(self):
        """
        get the value of property _Step
        """
        if self.force_auto_sync:
            self.get('Step')
        return self._Step

    @property
    def VlanIdList(self):
        """
        get the value of property _VlanIdList
        """
        if self.force_auto_sync:
            self.get('VlanIdList')
        return self._VlanIdList

    @property
    def Priority(self):
        """
        get the value of property _Priority
        """
        if self.force_auto_sync:
            self.get('Priority')
        return self._Priority

    @property
    def PriorityStep(self):
        """
        get the value of property _PriorityStep
        """
        if self.force_auto_sync:
            self.get('PriorityStep')
        return self._PriorityStep

    @property
    def PriorityList(self):
        """
        get the value of property _PriorityList
        """
        if self.force_auto_sync:
            self.get('PriorityList')
        return self._PriorityList

    @property
    def Cfi(self):
        """
        get the value of property _Cfi
        """
        if self.force_auto_sync:
            self.get('Cfi')
        return self._Cfi

    @property
    def Tpid(self):
        """
        get the value of property _Tpid
        """
        if self.force_auto_sync:
            self.get('Tpid')
        return self._Tpid

    @VlanId.setter
    def VlanId(self, value):
        self._VlanId = value
        self.edit(VlanId=value)

    @Step.setter
    def Step(self, value):
        self._Step = value
        self.edit(Step=value)

    @VlanIdList.setter
    def VlanIdList(self, value):
        self._VlanIdList = value
        self.edit(VlanIdList=value)

    @Priority.setter
    def Priority(self, value):
        self._Priority = value
        self.edit(Priority=value)

    @PriorityStep.setter
    def PriorityStep(self, value):
        self._PriorityStep = value
        self.edit(PriorityStep=value)

    @PriorityList.setter
    def PriorityList(self, value):
        self._PriorityList = value
        self.edit(PriorityList=value)

    @Cfi.setter
    def Cfi(self, value):
        self._Cfi = value
        self.edit(Cfi=value)

    @Tpid.setter
    def Tpid(self, value):
        self._Tpid = value
        self.edit(Tpid=value)

    def _set_vlanid_with_str(self, value):
        try:
            self._VlanId = int(value)
        except ValueError:
            self._VlanId = hex(int(value, 16))

    def _set_step_with_str(self, value):
        try:
            self._Step = int(value)
        except ValueError:
            self._Step = hex(int(value, 16))

    def _set_vlanidlist_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._VlanIdList = []
        values = tmp_value.split()
        for str_value in values:
            try:
                self._VlanIdList.append(int(str_value))
            except ValueError:
                self._VlanIdList.append(hex(int(str_value, 16)))

    def _set_priority_with_str(self, value):
        try:
            self._Priority = int(value)
        except ValueError:
            self._Priority = hex(int(value, 16))

    def _set_prioritystep_with_str(self, value):
        try:
            self._PriorityStep = int(value)
        except ValueError:
            self._PriorityStep = hex(int(value, 16))

    def _set_prioritylist_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._PriorityList = []
        values = tmp_value.split()
        for str_value in values:
            try:
                self._PriorityList.append(int(str_value))
            except ValueError:
                self._PriorityList.append(hex(int(str_value, 16)))

    def _set_cfi_with_str(self, value):
        self._Cfi = (value == 'True')

    def _set_tpid_with_str(self, value):
        try:
            self._Tpid = int(value)
        except ValueError:
            self._Tpid = hex(int(value, 16))

