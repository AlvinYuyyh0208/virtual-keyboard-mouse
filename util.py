
import platform

if platform.system() == 'Windows':
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import cast, POINTER
    # 控制设备音响硬件
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # print(volume.GetMasterVolumeLevel())
    # 音量范围
    volRan = volume.GetVolumeRange()
    volume.SetMasterVolumeLevel(-1.0, None)

    def increaseVolume():
        vol = volume.GetMasterVolumeLevel()
        volume.SetMasterVolumeLevel(vol + 1, None)

    def decreaseVolume():
        vol = volume.GetMasterVolumeLevel()
        volume.SetMasterVolumeLevel(vol - 1, None)
else:
    def increaseVolume():
        print('increaseVolume')

    def decreaseVolume():
        print('decreaseVolume')

__all__ = ['increaseVolume', 'decreaseVolume']
