// ================================
// مدیریت سوالات آزمون - create_quiz.js
// ================================

let editQuestions = []; // سوالات جدید اضافه شده
let editingIndex = null; // اندیس سوالی که در حال ویرایش است

// افزودن سوال جدید
function addQuestion() {
    const editor = document.getElementById("editQuestionEditor");
    const optionsContainer = document.getElementById("editOptionsContainer");
    const questionInput = document.getElementById("editQuestionText");

    editor.style.display = "block";
    questionInput.value = "";
    optionsContainer.innerHTML = "";

    // ایجاد 4 گزینه خالی با رادیو
    for (let i = 0; i < 4; i++) {
        const div = document.createElement("div");
        div.classList.add("option-item");

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "editCorrectOption";
        radio.value = i;

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = `گزینه ${i + 1}`;

        div.appendChild(radio);
        div.appendChild(input);
        optionsContainer.appendChild(div);
    }

    editingIndex = null; // اضافه کردن سوال جدید
}

// ذخیره سوال جدید یا ویرایش شده
function saveEditQuestion() {
    const questionText = document.getElementById("editQuestionText").value.trim();
    const optionsContainer = document.getElementById("editOptionsContainer");
    const optionItems = optionsContainer.querySelectorAll(".option-item");

    const options = [];
    let correctOption = null;

    optionItems.forEach((item, idx) => {
        const input = item.querySelector("input[type=text]");
        const radio = item.querySelector("input[type=radio]");
        if (input.value.trim() !== "") options.push(input.value.trim());
        if (radio.checked) correctOption = idx;
    });

    if (!questionText || options.length < 2 || correctOption === null) {
        alert("لطفاً متن سوال، حداقل دو گزینه و یک جواب صحیح انتخاب کنید.");
        return;
    }

    const questionData = { text: questionText, options, correct: correctOption };

    if (editingIndex !== null) editQuestions[editingIndex] = questionData;
    else editQuestions.push(questionData);

    renderEditQuestions();
    document.getElementById("editQuestionEditor").style.display = "none";
}

// نمایش پیش‌نمایش سوالات
function renderEditQuestions() {
    const list = document.getElementById("editQuestionsList");
    list.innerHTML = "";

    editQuestions.forEach((q, index) => {
        let html = `<div class="question-item">
            <p><strong>سؤال ${index + 1}:</strong> ${q.text}</p>
            <ul>`;
        q.options.forEach((opt, i) => {
            html += `<li>${opt} ${i === q.correct ? "✅" : ""}</li>`;
        });
        html += `</ul>
            <button type="button" onclick="editQuestion(${index})">✏️ ویرایش</button>
            <button type="button" onclick="deleteQuestion(${index})">🗑️ حذف</button>
        </div>`;
        list.innerHTML += html;
    });

    const counter = document.getElementById("editQuestionCountDisplay");
    if (counter) counter.textContent = editQuestions.length;
}

// ویرایش سوال موجود
function editQuestion(index) {
    editingIndex = index;
    const q = editQuestions[index];
    const editor = document.getElementById("editQuestionEditor");
    const questionInput = document.getElementById("editQuestionText");
    const optionsContainer = document.getElementById("editOptionsContainer");

    questionInput.value = q.text;
    optionsContainer.innerHTML = "";

    q.options.forEach((opt, i) => {
        const div = document.createElement("div");
        div.classList.add("option-item");

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "editCorrectOption";
        radio.value = i;
        if (i === q.correct) radio.checked = true;

        const input = document.createElement("input");
        input.type = "text";
        input.value = opt;

        div.appendChild(radio);
        div.appendChild(input);
        optionsContainer.appendChild(div);
    });

    editor.style.display = "block";
}

// حذف سوال
function deleteQuestion(index) {
    if (!confirm("آیا از حذف سوال مطمئن هستید؟")) return;
    editQuestions.splice(index, 1);
    renderEditQuestions();
}

// انصراف از ویرایش/افزودن سوال
function cancelEditQuestion() {
    document.getElementById("editQuestionEditor").style.display = "none";
}
