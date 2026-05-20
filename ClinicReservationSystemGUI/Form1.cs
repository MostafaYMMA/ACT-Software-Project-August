namespace ClinicReservationSystemGUI
{
    public partial class F : Form
    {
        List<int> ratings = new List<int>();
        List<int> bookings = new List<int>();
        List<string> doctors = new List<string>();
        public F()
        {
            InitializeComponent();

            doctors.Add("Dr. Alice Smith - Cardiology");
            doctors.Add("Dr. Bob Jones - Pediatrics");

            bookings.Add(0);
            bookings.Add(0);

            RefreshDoctors();
        }
        private void RefreshDoctors()
        {
            listBoxDoctors.Items.Clear();

            foreach (var doc in doctors)
            {
                listBoxDoctors.Items.Add(doc);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string name = txtName.Text;
            string email = txtEmail.Text;

            MessageBox.Show("Patient Registered:\nName: " + name + "\nEmail: " + email);
        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void btnBook_Click(object sender, EventArgs e)
        {
            if (listBoxDoctors.SelectedItem != null)
            {
                MessageBox.Show("Appointment booked with:\n" +
                                listBoxDoctors.SelectedItem.ToString());
            }
            else
            {
                MessageBox.Show("Please select a doctor first.");
            }

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void btnAddPractitioner_Click(object sender, EventArgs e)
        {
            string clinic = txtClinicName.Text;
            string address = txtAddress.Text;
            string price = txtPrice.Text;
            string department = txtDepartment.Text;
            string schedule = txtSchedule.Text;

            listBoxDoctors.Items.Add(
                "Dr. " + txtName.Text +
                " - " + department +
                " | " + clinic
            );

            MessageBox.Show("Practitioner added successfully!");
        }

        private void btnFilter_Click(object sender, EventArgs e)
        {
            string dept = txtFilterDepartment.Text.ToLower();

            listBoxDoctors.Items.Clear();

            if (dept == "cardiology")
            {
                listBoxDoctors.Items.Add("Dr. Alice Smith - Cardiology");
            }
            else if (dept == "pediatrics")
            {
                listBoxDoctors.Items.Add("Dr. Bob Jones - Pediatrics");
            }
            else
            {
                MessageBox.Show("No practitioners found.");
            }
        }

        private void btnReport_Click(object sender, EventArgs e)
        {
            if (listBoxDoctors.Items.Count == 0)
            {
                MessageBox.Show("No practitioners available.");
                return;
            }

            string report = "===== SYSTEM STATISTICS REPORT =====\n\n";

            report += "Total Practitioners: " + listBoxDoctors.Items.Count + "\n\n";

            report += "Practitioners List:\n";

            foreach (var doc in listBoxDoctors.Items)
            {
                report += "- " + doc.ToString() + "\n";
            }

            report += "\n===================================";

            MessageBox.Show(report, "Statistics Report");
        }

        private void btnRate_Click(object sender, EventArgs e)
        {
            if (listBoxDoctors.SelectedItem == null)
            {
                MessageBox.Show("Please select a doctor first.");
                return;
            }

            if (!int.TryParse(txtRating.Text, out int rating))
            {
                MessageBox.Show("Enter a valid number (1 to 5).");
                return;
            }

            if (rating < 1 || rating > 5)
            {
                MessageBox.Show("Rating must be between 1 and 5.");
                return;
            }

            ratings.Add(rating);

            MessageBox.Show("Rating submitted successfully!");
        }
    }
}