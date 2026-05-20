namespace ClinicReservationSystemGUI
{
    partial class F
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            txtName = new TextBox();
            label2 = new Label();
            txtEmail = new TextBox();
            button1 = new Button();
            listBoxDoctors = new ListBox();
            btnBook = new Button();
            label3 = new Label();
            label4 = new Label();
            label5 = new Label();
            label6 = new Label();
            label7 = new Label();
            txtClinicName = new TextBox();
            txtAddress = new TextBox();
            txtPrice = new TextBox();
            txtDepartment = new TextBox();
            txtSchedule = new TextBox();
            btnAddPractitioner = new Button();
            label8 = new Label();
            txtFilterDepartment = new TextBox();
            btnFilter = new Button();
            btnReport = new Button();
            txtRating = new TextBox();
            btnRate = new Button();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(8, 3);
            label1.Name = "label1";
            label1.Size = new Size(49, 20);
            label1.TabIndex = 0;
            label1.Text = "Name";
            // 
            // txtName
            // 
            txtName.Location = new Point(75, 8);
            txtName.Name = "txtName";
            txtName.Size = new Size(125, 27);
            txtName.TabIndex = 1;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(16, 45);
            label2.Name = "label2";
            label2.Size = new Size(46, 20);
            label2.TabIndex = 2;
            label2.Text = "Email";
            // 
            // txtEmail
            // 
            txtEmail.Location = new Point(75, 45);
            txtEmail.Name = "txtEmail";
            txtEmail.Size = new Size(125, 27);
            txtEmail.TabIndex = 3;
            // 
            // button1
            // 
            button1.Location = new Point(18, 89);
            button1.Name = "button1";
            button1.Size = new Size(172, 29);
            button1.TabIndex = 4;
            button1.Text = "Register Ptatient";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // listBoxDoctors
            // 
            listBoxDoctors.FormattingEnabled = true;
            listBoxDoctors.Location = new Point(22, 144);
            listBoxDoctors.Name = "listBoxDoctors";
            listBoxDoctors.Size = new Size(150, 104);
            listBoxDoctors.TabIndex = 5;
            listBoxDoctors.SelectedIndexChanged += listBox1_SelectedIndexChanged;
            // 
            // btnBook
            // 
            btnBook.Location = new Point(33, 262);
            btnBook.Name = "btnBook";
            btnBook.Size = new Size(139, 29);
            btnBook.TabIndex = 6;
            btnBook.Text = "book appointemt";
            btnBook.UseVisualStyleBackColor = true;
            btnBook.Click += btnBook_Click;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(245, 8);
            label3.Name = "label3";
            label3.Size = new Size(84, 20);
            label3.TabIndex = 7;
            label3.Text = "clinic name";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(245, 38);
            label4.Name = "label4";
            label4.Size = new Size(60, 20);
            label4.TabIndex = 8;
            label4.Text = "address";
            label4.Click += label4_Click;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Location = new Point(245, 78);
            label5.Name = "label5";
            label5.Size = new Size(42, 20);
            label5.TabIndex = 9;
            label5.Text = "price";
            label5.Click += label5_Click;
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Location = new Point(240, 107);
            label6.Name = "label6";
            label6.Size = new Size(89, 20);
            label6.TabIndex = 10;
            label6.Text = "Department";
            label6.Click += label6_Click;
            // 
            // label7
            // 
            label7.AutoSize = true;
            label7.Location = new Point(245, 153);
            label7.Name = "label7";
            label7.Size = new Size(69, 20);
            label7.TabIndex = 11;
            label7.Text = "Schedule";
            // 
            // txtClinicName
            // 
            txtClinicName.Location = new Point(335, 3);
            txtClinicName.Name = "txtClinicName";
            txtClinicName.Size = new Size(125, 27);
            txtClinicName.TabIndex = 12;
            // 
            // txtAddress
            // 
            txtAddress.Location = new Point(335, 35);
            txtAddress.Name = "txtAddress";
            txtAddress.Size = new Size(125, 27);
            txtAddress.TabIndex = 13;
            // 
            // txtPrice
            // 
            txtPrice.Location = new Point(335, 68);
            txtPrice.Name = "txtPrice";
            txtPrice.Size = new Size(125, 27);
            txtPrice.TabIndex = 14;
            // 
            // txtDepartment
            // 
            txtDepartment.Location = new Point(335, 107);
            txtDepartment.Name = "txtDepartment";
            txtDepartment.Size = new Size(125, 27);
            txtDepartment.TabIndex = 15;
            // 
            // txtSchedule
            // 
            txtSchedule.Location = new Point(341, 153);
            txtSchedule.Name = "txtSchedule";
            txtSchedule.Size = new Size(125, 27);
            txtSchedule.TabIndex = 16;
            // 
            // btnAddPractitioner
            // 
            btnAddPractitioner.Location = new Point(254, 207);
            btnAddPractitioner.Name = "btnAddPractitioner";
            btnAddPractitioner.Size = new Size(155, 29);
            btnAddPractitioner.TabIndex = 17;
            btnAddPractitioner.Text = "Add Partitioner";
            btnAddPractitioner.UseVisualStyleBackColor = true;
            btnAddPractitioner.Click += btnAddPractitioner_Click;
            // 
            // label8
            // 
            label8.AutoSize = true;
            label8.Location = new Point(259, 260);
            label8.Name = "label8";
            label8.Size = new Size(89, 20);
            label8.TabIndex = 18;
            label8.Text = "Department";
            // 
            // txtFilterDepartment
            // 
            txtFilterDepartment.Location = new Point(361, 262);
            txtFilterDepartment.Name = "txtFilterDepartment";
            txtFilterDepartment.Size = new Size(125, 27);
            txtFilterDepartment.TabIndex = 19;
            // 
            // btnFilter
            // 
            btnFilter.Location = new Point(270, 301);
            btnFilter.Name = "btnFilter";
            btnFilter.Size = new Size(84, 29);
            btnFilter.TabIndex = 20;
            btnFilter.Text = "Filter";
            btnFilter.UseVisualStyleBackColor = true;
            btnFilter.Click += btnFilter_Click;
            // 
            // btnReport
            // 
            btnReport.Location = new Point(516, 7);
            btnReport.Name = "btnReport";
            btnReport.Size = new Size(185, 29);
            btnReport.TabIndex = 21;
            btnReport.Text = "view statics report";
            btnReport.UseVisualStyleBackColor = true;
            btnReport.Click += btnReport_Click;
            // 
            // txtRating
            // 
            txtRating.Location = new Point(636, 68);
            txtRating.Name = "txtRating";
            txtRating.Size = new Size(125, 27);
            txtRating.TabIndex = 22;
            // 
            // btnRate
            // 
            btnRate.Location = new Point(507, 66);
            btnRate.Name = "btnRate";
            btnRate.Size = new Size(123, 29);
            btnRate.TabIndex = 23;
            btnRate.Text = "Rate Doctor";
            btnRate.UseVisualStyleBackColor = true;
            btnRate.Click += btnRate_Click;
            // 
            // F
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(btnRate);
            Controls.Add(txtRating);
            Controls.Add(btnReport);
            Controls.Add(btnFilter);
            Controls.Add(txtFilterDepartment);
            Controls.Add(label8);
            Controls.Add(btnAddPractitioner);
            Controls.Add(txtSchedule);
            Controls.Add(txtDepartment);
            Controls.Add(txtPrice);
            Controls.Add(txtAddress);
            Controls.Add(txtClinicName);
            Controls.Add(label7);
            Controls.Add(label6);
            Controls.Add(label5);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(btnBook);
            Controls.Add(listBoxDoctors);
            Controls.Add(button1);
            Controls.Add(txtEmail);
            Controls.Add(label2);
            Controls.Add(txtName);
            Controls.Add(label1);
            Name = "F";
            Text = "Form1";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private TextBox txtName;
        private Label label2;
        private TextBox txtEmail;
        private Button button1;
        private ListBox listBoxDoctors;
        private Button btnBook;
        private Label label3;
        private Label label4;
        private Label label5;
        private Label label6;
        private Label label7;
        private TextBox txtClinicName;
        private TextBox txtAddress;
        private TextBox txtPrice;
        private TextBox txtDepartment;
        private TextBox txtSchedule;
        private Button btnAddPractitioner;
        private Label label8;
        private TextBox txtFilterDepartment;
        private Button btnFilter;
        private Button btnReport;
        private TextBox txtRating;
        private Button btnRate;
    }
}
