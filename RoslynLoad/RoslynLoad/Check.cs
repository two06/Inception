using System;
using Microsoft.Win32;

namespace RoslynLoad
{
    public  class Check
    {
        public static bool RunCheck()
        {
            var MinimumUSBHistory = 2;
            var MinimumBrowserCount = 2;
            var browserCount = 0;
            try
            {
                var OpenedKey = Registry.LocalMachine.OpenSubKey(@"SYSTEM\ControlSet001\Enum\USBSTOR", false);

                if (OpenedKey.GetSubKeyNames().Length <= MinimumUSBHistory)
                {
                    return false;
                }

                string[] browserKeys = { @"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe", @"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\iexplore.exe", @"SOFTWARE\Mozilla" };

                foreach (var browserKey in browserKeys)
                {
                    OpenedKey = Registry.LocalMachine.OpenSubKey(browserKey, false);
                    if (OpenedKey != null)
                    {
                        browserCount += 1;
                    }
                }

                if (browserCount >= MinimumBrowserCount)
                {
                    return true;
                }
                return false;
            }
            catch
            {
                return false;
            }
            
        }
    }
}
