let quizzes = [];
let currentQuestions = [];
let editingQuestionIndex = null;

const dashboardUrl = "/professor/dashboard/";
const createUrl = "/professor/dashboard/create_quiz/";
const modal = document.getElementById("createModal");
const container = document.getElementById("modalFormContainer");

document.addEventListener("DOMContentLoaded", function () {
    initializeQuestionEditor();
    updateStats();
    renderQuizzes();

    // ---- اگر رفرش شد و مودال باز بود، مودال را ببند و URL را به داشبورد برگردان ----
    if (window.location.pathname === createUrl) {
        // شبیه Back: مودال بسته شود و URL به داشبورد برگردد
        hideModal();
        window.history.replaceState({}, "", dashboardUrl);
    }

    // مدیریت Back/Forward مرورگر
    window.addEventListener("popstate", function (event) {
        const modalOpen = event.state && event.state.modalOpen;
        if (modalOpen) {
            showModal();
            loadCreateQuizForm();
        } else {
            hideModal();
        }
    });
});

// ---- باز کردن مودال توسط کاربر ----
function openCreateModal() {
    showModal();
    // pushState فقط وقتی کاربر کلیک می‌کند
    window.history.pushState({ modalOpen: true }, "", createUrl);
    loadCreateQuizForm();
}

// ---- بستن مودال توسط کاربر ----
function closeCreateModal() {
    hideModal();
    window.history.pushState({ modalOpen: false }, "", dashboardUrl);
}

// ---- نمایش/مخفی کردن مودال ----
function showModal() {
    if (!modal) return;
    modal.classList.add("show");
}

function hideModal() {
    if (!modal) return;
    modal.classList.remove("show");
    if (container) container.innerHTML = ""; // فرم را پاک کن
}

// ---- لود فرم با GET ----
function loadCreateQuizForm() {
    if (!container) return;
    fetch(createUrl, { method: "GET" })
        .then(res => res.text())
        .then(html => { container.innerHTML = html; })
        .catch(err => console.error("Error loading form:", err));
}


// ---- افزودن سوال ----
function addQuestion() {
    document.getElementById("questionEditor").style.display = "block";
    document.getElementById("questionText").value = "";

    // ریست کردن گزینه‌ها
    const optionsContainer = document.getElementById("optionsContainer");
    optionsContainer.innerHTML = "";
    for (let i = 0; i < 4; i++) {
        const optionItem = document.createElement("div");
        optionItem.classList.add("option-item");

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "correctOption";
        radio.value = i;

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = `گزینه ${i + 1}`;

        optionItem.appendChild(radio);
        optionItem.appendChild(input);
        optionsContainer.appendChild(optionItem);
    }
}

// ---- ذخیره سوال موقت ----
function saveQuestion() {
    const questionText = document.getElementById("questionText").value.trim();
    const options = [];
    let correctOption = null;

    const optionItems = document.querySelectorAll("#optionsContainer .option-item");
    optionItems.forEach((item, index) => {
        const textInput = item.querySelector("input[type='text']");
        const radioInput = item.querySelector("input[type='radio']");
        if (textInput.value.trim() !== "") {
            options.push(textInput.value.trim());
            if (radioInput.checked) correctOption = index;
        }
    });

    if (!questionText || options.length < 2) {
        alert("لطفاً متن سؤال و حداقل دو گزینه را وارد کنید.");
        return;
    }
    if (correctOption === null) {
        alert("حداقل یک گزینه باید به عنوان جواب درست انتخاب شود.");
        return;
    }

    currentQuestions.push({
        text: questionText,
        options: options,
        correct: correctOption,
    });
    renderPreviewQuestions();
    document.getElementById("questionEditor").style.display = "none";
}

// ---- پیش‌نمایش سوالات ----
function renderPreviewQuestions() {
    const preview = document.getElementById("previewQuestions");
    if (!preview) return;
    preview.innerHTML = "";

    currentQuestions.forEach((q, index) => {
        let html = `<p><strong>سؤال ${index + 1}:</strong> ${q.text}</p><ul>`;
        q.options.forEach((opt, i) => {
            const mark = i === q.correct ? "✅" : "";
            html += `<li>${opt} ${mark}</li>`;
        });
        html += "</ul>";
        preview.innerHTML += html;
    });

    // شمارش سوالات + فعال/غیرفعال کردن دکمه
    const count = currentQuestions.length;
    const createBtn = document.getElementById("createQuizBtn");
    if (createBtn) {
        createBtn.disabled = count === 0;
        createBtn.innerText = `ایجاد آزمون (${count} سوال)`;
    }
    const counter = document.getElementById("questionCountDisplay");
    if (counter) counter.innerText = count;
}

// ---- سازگاری ----
function updateStats() {}
function renderQuizzes() {}
function initializeQuestionEditor() {}
function cancelQuestionEdit() {
    document.getElementById("questionEditor").style.display = "none";
}
function openEditModal(quizId = "") {
    showModal(); // تابعی که کلاس show به مودال اضافه می‌کند
    document.getElementById("modalTitle").textContent = "✏️ ویرایش آزمون";
    
    const editUrl = `/professor/dashboard/edit_quiz/${quizId}/`;

    // تغییر URL مرورگر برای back/forward
    window.history.pushState({ modalOpen: true }, "", editUrl);

    // GET برای گرفتن محتوای فرم
    fetch(editUrl, { method: "GET" })
        .then(res => res.text())
        .then(html => {
            document.getElementById("modalFormContainer").innerHTML = html;
        })
        .catch(err => console.error("Error loading edit form:", err));
}

//edit question
let editQuestions = [];
let editingIndex = null;

window.addEditQuestion = function() {
    const editor = document.getElementById("editQuestionEditor");
    const optionsContainer = document.getElementById("editOptionsContainer");
    const questionInput = document.getElementById("editQuestionText");

    if (!editor || !optionsContainer || !questionInput) return;

    editor.style.display = "block";
    questionInput.value = "";

    // ایجاد ۴ گزینه خالی با رادیو
    optionsContainer.innerHTML = "";
    for (let i = 0; i < 4; i++) {
        const optionDiv = document.createElement("div");
        optionDiv.classList.add("option-item");

        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "editCorrectOption";
        radio.value = i;

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = `گزینه ${i+1}`;

        optionDiv.appendChild(radio);
        optionDiv.appendChild(input);
        optionsContainer.appendChild(optionDiv);
    }

    editingIndex = null; // اضافه کردن سوال جدید
};

window.saveEditQuestion = function() {
    const questionInput = document.getElementById("editQuestionText");
    const optionsContainer = document.getElementById("editOptionsContainer");

    const questionText = questionInput.value.trim();
    const options = [];
    let correctOption = null;

    optionsContainer.querySelectorAll(".option-item").forEach((item, index) => {
        const textInput = item.querySelector("input[type=text]");
        const radio = item.querySelector("input[type=radio]");
        if (textInput.value.trim() !== "") options.push(textInput.value.trim());
        if (radio.checked) correctOption = index;
    });

    if (!questionText || options.length < 2) {
        alert("لطفاً متن سوال و حداقل دو گزینه وارد کنید.");
        return;
    }
    if (correctOption === null) {
        alert("حداقل یک گزینه باید به عنوان جواب درست انتخاب شود.");
        return;
    }

    const questionData = { text: questionText, options, correct: correctOption };

    if (editingIndex !== null) {
        editQuestions[editingIndex] = questionData;
    } else {
        editQuestions.push(questionData);
    }

    renderEditQuestions();
    document.getElementById("editQuestionEditor").style.display = "none";
};

window.cancelEditQuestion = function() {
    document.getElementById("editQuestionEditor").style.display = "none";
};

function renderEditQuestions() {
    const list = document.getElementById("editQuestionsList");
    const counter = document.getElementById("editQuestionCountDisplay");
    list.innerHTML = "";

    editQuestions.forEach((q, index) => {
        let html = `<div class="question-item">
            <p><strong>سؤال ${index+1}:</strong> ${q.text}</p>
            <ul>`;
        q.options.forEach((opt, i) => {
            const mark = i === q.correct ? "✅" : "";
            html += `<li>${opt} ${mark}</li>`;
        });
        html += `</ul>
            <button type="button" onclick="editQuestion(${index})">✏️ ویرایش</button>
            <button type="button" onclick="deleteQuestion(${index})">🗑️ حذف</button>
        </div>`;
        list.innerHTML += html;
    });

    if (counter) counter.textContent = editQuestions.length;
}

window.editQuestion = function(index) {
    const editor = document.getElementById("editQuestionEditor");
    const questionInput = document.getElementById("editQuestionText");
    const optionsContainer = document.getElementById("editOptionsContainer");

    const q = editQuestions[index];
    if (!q) return;

    editor.style.display = "block";
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

    editingIndex = index;
};

window.deleteQuestion = function(index) {
    if (!confirm("آیا از حذف سوال مطمئن هستید؟")) return;
    editQuestions.splice(index, 1);
    renderEditQuestions();
};