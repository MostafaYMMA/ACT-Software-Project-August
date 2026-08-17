let currentDate = new Date();
let selectedDate = null;

function renderCalendar() {

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthTitle = document.getElementById("calendarMonth");
  const calendarDays = document.getElementById("calendarDays");

  if (!monthTitle || !calendarDays) return;


  // اسم الشهر والسنة
  monthTitle.textContent = new Date(
    year,
    month,
    1
  ).toLocaleDateString("en-US", {
    month: "long",
    year: "numeric"
  });


  // أول يوم في الشهر
  const firstDay = new Date(
    year,
    month,
    1
  ).getDay();


  // عدد أيام الشهر
  const daysInMonth = new Date(
    year,
    month + 1,
    0
  ).getDate();


  calendarDays.innerHTML = "";


  // الأيام الفارغة قبل بداية الشهر
  for (let i = 0; i < firstDay; i++) {

    const emptyDay = document.createElement("div");

    emptyDay.className = "calendar-day empty";

    calendarDays.appendChild(emptyDay);
  }


  // تاريخ اليوم
  const today = new Date();


  // إنشاء الأيام
  for (let day = 1; day <= daysInMonth; day++) {

    const dayButton = document.createElement("button");

    dayButton.type = "button";
    dayButton.className = "calendar-day";
    dayButton.textContent = day;


    // تحديد اليوم الحالي
    if (
      day === today.getDate() &&
      month === today.getMonth() &&
      year === today.getFullYear()
    ) {
      dayButton.classList.add("today");
    }


    // تحديد اليوم الذي ضغط عليه المستخدم
    if (
      selectedDate &&
      selectedDate.day === day &&
      selectedDate.month === month &&
      selectedDate.year === year
    ) {
      dayButton.classList.add("selected");
    }


    // عند الضغط على يوم
    dayButton.addEventListener("click", function () {

      selectedDate = {
        day: day,
        month: month,
        year: year
      };

      renderCalendar();

    });


    calendarDays.appendChild(dayButton);
  }
}


// الشهر السابق
document.getElementById("prevMonth")?.addEventListener("click", function () {

  currentDate.setMonth(
    currentDate.getMonth() - 1
  );

  renderCalendar();

});


// الشهر التالي
document.getElementById("nextMonth")?.addEventListener("click", function () {

  currentDate.setMonth(
    currentDate.getMonth() + 1
  );

  renderCalendar();

});


// تشغيل الـ Calendar
renderCalendar();