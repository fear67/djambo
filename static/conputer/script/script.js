
var selected = null;
document.addEventListener('click', function (e) {
    
    // 1. Слайдер категорий на ГЛАВНОЙ (с возможностью СБРОСА)
    const sortBlock = e.target.closest('.sortblock');
    if (sortBlock) {
        const categoryName = sortBlock.querySelector('.sortname').textContent.trim();
        updateFilters('category_name', categoryName);
    }

    // 2. МОДАЛЬНЫЕ ОКНА (Общая логика)
    const isModalBtn = e.target.classList.contains('details') || e.target.classList.contains('info_btn');
    if (isModalBtn) {
        const modalId = e.target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    // Закрытие модалок
    if (e.target.classList.contains('close') || e.target.classList.contains('modal-overlay')) {
        const modal = e.target.closest('.modal-overlay');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // 3. Выбор КАТЕГОРИИ в Конфигураторе (Building)
    const btn = e.target.closest('.formbut');
    if (btn) {
        // Визуальная подсветка кнопки
        document.querySelectorAll('.formbut').forEach(el => el.style.backgroundColor = '#26262694');
        btn.style.backgroundColor = '#26262634';
        
        const fieldName = btn.getAttribute('data-field');
        const text = btn.querySelector('.label-text').textContent.trim();
        let cleanText = text.replace(/[0-9]/g, '').trim();
        if (!text.includes("Количество")) {
            sendSort(cleanText, fieldName);
        }
    }

const card = e.target.closest('.js-build-card');
if (card) {
    const urlParams = new URLSearchParams(window.location.search);
    const fieldName = urlParams.get('active_field');
    if (fieldName) {
        const componentId = card.getAttribute('data-id');
        const componentName = card.getAttribute('data-name');
        const componentPrice = card.getAttribute('data-price'); // 1. Вытаскиваем цену

        const select = document.querySelector(`select[name="${fieldName}"]`);
        if (select) {
            select.value = componentId;
            console.log(1)
            localStorage.setItem('build_' + fieldName, componentId);
            localStorage.setItem('name_' + fieldName, componentName);
            localStorage.setItem('price_' + fieldName, componentPrice); // 2. Сохраняем цену в память
            
            const displayVal = document.getElementById('val-' + fieldName);
            if (displayVal) {
                displayVal.textContent = componentName;
            }

            // 3. Запускаем пересчет суммы сразу после выбора
            calculateTotal(); 
        }
    } else {
        alert("Сначала выберите категорию (кнопку) слева!");
    }
}

    const clear = e.target.closest('.clearBuild');
    if (clear) {
        if (confirm('Вы уверены, что хотите выполнить это действие?')) {
            localStorage.clear();
            e.preventDefault(); 
            window.location.href = window.location.pathname; 
        }
    }

    const startbuild = e.target.closest('.js-start-build');
    if (startbuild) {
        localStorage.clear();

        const id = e.target.getAttribute('data-id');
        const name = e.target.getAttribute('data-name');
        const cat = e.target.getAttribute('data-field');

        console.log("Добавляю:", cat, name, id); // Проверь это в консоли F12!

        const categoryToField = {
            'Процессор': 'cpu',
            'Видеокарта': 'gpu',
            'Материнская плата': 'motherboard',
            'Оперативная память': 'ram',
            'Блок питания': 'powerSupply',
            'Корпус': 'case',
            'Накопитель': 'storage_primary',
            'Кулер для процессора': 'cooller',       // Исправил под модель
            'Корпусный вентилятор': 'coollerCase'   // Добавил, чтобы вентиляторы тоже работали
        };

        const fieldName = categoryToField[cat] || cat;
        localStorage.setItem('build_' + fieldName, id);
        localStorage.setItem('name_' + fieldName, name);

        window.location.href = '/building/';
    }
});

function updateFilters(key, value) {
    const url = new URL(window.location.href);
    if (url.searchParams.get(key) === value) {
        url.searchParams.delete(key);
    } else {
        url.searchParams.set(key, value);
    }
    window.location.href = url.toString();
}

function sendSort(text, fieldName) {
    const url = new URL(window.location.href);
    url.searchParams.set('category_name', text);
    if (fieldName) url.searchParams.set('active_field', fieldName);
    window.location.href = url.toString();
}


document.addEventListener('input', function (e) {
    if (e.target.name === 'title' || e.target.name === 'user_name') {
        localStorage.setItem('build_' + e.target.name, e.target.value);
    }
});

function restoreBuildData() {
    const fields = ['cpu', 'gpu', 'motherboard', 'ram', 'powerSupply', 'case', 'storage_primary', 'storage_second', 'cooller', 'coollerCase'];
    
    fields.forEach(field => {
        const select = document.querySelector(`select[name="${field}"]`);
        const displayVal = document.getElementById('val-' + field);
        
        // 1. Берем ID из памяти (который записала кнопка "Добавить в сборку")
        let savedId = localStorage.getItem('build_' + field);
        let savedName = localStorage.getItem('name_' + field);

        // 2. Если в памяти есть данные — ПРИНУДИТЕЛЬНО вставляем их в форму
        if (savedId && select) {
            select.value = savedId;
            if (displayVal && savedName) {
                displayVal.textContent = savedName;
            }
        } 
        // 3. Если в памяти пусто, но мы в режиме редактирования (Django заполнил форму)
        else if (!savedId && select && select.value) {
            savedName = select.options[select.selectedIndex].text;
            if (displayVal) displayVal.textContent = savedName;
        }
    });
}

window.addEventListener('load', restoreBuildData);

const postForm = document.querySelector('form[method="POST"]');
if (postForm) {
    postForm.addEventListener('submit', function() {
        localStorage.clear();
    });
}

function previewImage(input) {
    const previewBox = document.getElementById('photopreviewbox');
    const previewImg = document.getElementById('image-preview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'flex';
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function calculateTotal() {
    let total = 0;
    // Список всех полей, где может быть цена
    const fields = ['cpu', 'gpu', 'motherboard', 'ram', 'powerSupply', 'case', 'storage_primary', 'storage_second', 'cooller', 'coollerCase'];
    
    fields.forEach(field => {
        // Достаем цену из памяти, переводим в число (или 0, если пусто)
        const price = parseInt(localStorage.getItem('price_' + field)) || 0;
        total += price;
    });

    // Ищем твой блок с id="total-price" и пишем туда сумму
    const totalDisplay = document.getElementById('total-price');
    if (totalDisplay) {
        // toLocaleString() добавит красивые пробелы между тысячами (10 000 вместо 10000)
        totalDisplay.textContent = total.toLocaleString() + ' ₽';
    }
}

window.addEventListener('load', calculateTotal);