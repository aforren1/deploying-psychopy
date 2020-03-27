using System;
using System.Diagnostics;
using System.Windows.Forms;
using System.IO;
// https://stackoverflow.com/questions/45309093/running-external-executable-from-c-sharp-solution-with-relative-path
class Launcher {
    static void Main() {
        Process p = new Process();
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.FileName = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "main", @"main.exe");
        p.Start();
    }
}
