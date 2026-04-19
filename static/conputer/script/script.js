
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

    // 4. Выбор КОМПОНЕНТА из списка (Building)
    const card = e.target.closest('.js-build-card');
    if (card) {
        // Восстанавливаем активное поле из URL
        const urlParams = new URLSearchParams(window.location.search);
        const fieldName = urlParams.get('active_field');

        if (fieldName) {
            const componentId = card.getAttribute('data-id');
            const componentName = card.getAttribute('data-name');
            
            // Записываем в скрытый select Django
            const select = document.querySelector(`select[name="${fieldName}"]`);
            if (select) {
                select.value = componentId;
                
                // Сохраняем выбор в память (localStorage)
                localStorage.setItem('build_' + fieldName, componentId);
                localStorage.setItem('name_' + fieldName, componentName);
                
                // Обновляем текст на странице (span "Не выбрано")
                const displayVal = document.getElementById('val-' + fieldName);
                if (displayVal) {
                    displayVal.textContent = componentName;
                }
            }
        } else {
            alert("Сначала выберите категорию (кнопку) слева!");
        }
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
    const fields = ['title', 'user_name', 'cpu', 'gpu', 'motherboard', 'ram', 'powerSupply', 'case', 'storage_primary', 'storage_second', 'cooller', 'coollerCase'];
    
    fields.forEach(field => {
        const savedValue = localStorage.getItem('build_' + field);
        const savedName = localStorage.getItem('name_' + field);
        
        const element = document.querySelector(`[name="${field}"]`);
        if (element && savedValue) {
            element.value = savedValue;
        }

        const displayVal = document.getElementById('val-' + field);
        if (displayVal && savedName) {
            displayVal.textContent = savedName;
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

