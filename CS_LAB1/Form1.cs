using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace CS_LAB1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string filePath = @"E:\Audit Policiy\To Work\CIS_DC_SERVER_2012_Level_1_v2.2.0.audit";
            string filePath1= @"E:\Audit Policiy\To Work\CIS_DC_SERVER_2012_Level_2_v2.2.0.audit";
            string filePath2 = @"E:\Audit Policiy\To Work\CIS_DC_SERVER_2012_R2_Level_1_v2.4.0.audit";

            string destinationPath = @"E:\Audit Policiy\To Work\Replaced\Audit_1.json";
            string destinationPath1 = @"E:\Audit Policiy\To Work\Replaced\Audit_2.json";
            string destinationPath2 = @"E:\Audit Policiy\To Work\Replaced\Audit_3.json";


            List<string> lines = new List<string>();
            lines = File.ReadAllLines(filePath).ToList();




        foreach (string line in lines)
        {
            Console.WriteLine(line);
        }
        ///////////////////////////////////////////////////////////////////// 
            try
            {
                if (File.Exists(destinationPath))
                {
                    File.Delete(destinationPath);
                }

                using (StreamWriter sw = File.CreateText(destinationPath))
                {
                    foreach(string line in lines)
                    {
                        sw.WriteLine(line);
                    }
                }
            }
            catch(Exception Ex)
            {
                Console.WriteLine(Ex.ToString());
            }
            ///////////////////////////////////////////////////////////
            try
            {
                List<string> lines1 = new List<string>();
                lines1 = File.ReadAllLines(filePath1).ToList();
                if (File.Exists(destinationPath1))
                {
                    File.Delete(destinationPath1);
                }

                using (StreamWriter sw = File.CreateText(destinationPath1))
                {
                    foreach (string line in lines1)
                    {
                        sw.WriteLine(line);
                    }
                }
            }
            catch (Exception Ex)
            {
                Console.WriteLine(Ex.ToString());
            }
            //////////////////////////////////////////////////////////////
            try
            {
                List<string> lines2 = new List<string>();
                lines2 = File.ReadAllLines(filePath2).ToList();

                if (File.Exists(destinationPath2))
                {
                    File.Delete(destinationPath2);
                }

                using (StreamWriter sw = File.CreateText(destinationPath2))
                {
                    foreach (string line in lines2)
                    {
                        sw.WriteLine(line);
                    }
                }
            }
            catch (Exception Ex)
            {
                Console.WriteLine(Ex.ToString());
            }
            MessageBox.Show("Convertion done.\n Path: E:\\Audit Policiy\\To Work\\Replaced", "Done", MessageBoxButtons.OK, MessageBoxIcon.Information);
            Console.ReadLine();
            
        }

     

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
