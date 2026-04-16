// function scrollSlider(distance) {
//     const slider = document.getElementById('slider');
//     if (slider) {
//         slider.scrollBy({
//             left: distance,
//             behavior: 'smooth'
//         });
//     }
// }
var selected = null;
document.addEventListener('click',function(e)
{
    console.log(e.target)
    console.log(e.target.classList)
    if(e.target.classList.contains('sortblock'))
    {
        elems = document.querySelectorAll('.sortblock');
        elems.forEach(element => {
            element.style.backgroundColor = ' rgba(255, 255, 255, 0)'
        });
        e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.36)';
        const pa = e.target.querySelector('.sortname');
        selected = e.target;
        console.log(pa.textContent);
        sendSort(pa.textContent);
    }

    if (e.target.classList.contains('details')) {
        const modalId = e.target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    if (e.target.classList.contains('close') || e.target.classList.contains('modal-overlay')) {
        const modal = e.target.closest('.modal-overlay');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    if (e.target.classList.contains('info_btn')) {
        console.log("wow");
        const modalId = e.target.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('close')) {
        const modal = e.target.closest('.modal-overlay');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    const btn = e.target.closest('.formbut');

    if(btn)
    {
        elems = document.querySelectorAll('.formbut');
        elems.forEach(element => {
            element.style.backgroundColor = ' #26262694'
        });

        e.target.style.backgroundColor = '#26262634';

        selected = e.target;

        const fieldName = btn.getAttribute('data-field');
        const text = btn.querySelector('.label-text').textContent.trim();

        if (e.target.textContent.includes("Количество")) {
            return;
        }
        sendSort(text, fieldName);
    }


    const card = e.target.closest('.js-build-card');

    if (card) 
    {
        const urlParams = new URLSearchParams(window.location.search);
        window.currentBuildingField = urlParams.get('active_field');

        if (window.currentBuildingField) {
         console.log("Память восстановлена! Активное поле:", window.currentBuildingField);
        }
        const componentId = card.getAttribute('data-id');
        const componentName = card.getAttribute('data-name');
        const fieldName = window.currentBuildingField;

        console.log("Пытаюсь записать в поле:", fieldName);

        if (fieldName) {
            // Запись в скрытый селект
            const select = document.querySelector(`select[name="${fieldName}"]`);
           if (select) {
                select.value = componentId;
                localStorage.setItem('build_' + fieldName, componentId);
                localStorage.setItem('name_' + fieldName, componentName);
            }

            // Обновление текста
            const displayVal = document.getElementById('val-' + fieldName);
            if (displayVal) {
                displayVal.textContent = componentName;
                console.log("Текст успешно изменен на:", componentName);
            } else {
                console.error("Не нашел span с ID:", 'val-' + fieldName);
            }
        } else {
            console.warn("Поле не выбрано! Сначала нажми на кнопку слева.");
        }
    }


})

function sendSort(text, fieldName) {
    const url = new URL(window.location.href);
    
    url.searchParams.set('category_name', text);
    url.searchParams.set('active_field', fieldName);
    
    window.location.href = url.toString();
}

function updateFilters(key, value) {
    const url = new URL(window.location.href);
    
    if (url.searchParams.get(key) === value) {
        url.searchParams.delete(key);
    } else {
        url.searchParams.set(key, value);
    }
    
    window.location.href = url.toString();
}


function pick(id, name) {
    // 1. Устанавливаем значение в скрытый select Django
    const select = document.getElementsByName(currentField)[0];
    select.value = id;

    // 2. Обновляем визуальный текст в левой колонке
    document.getElementById('val-' + currentField).textContent = name;
}


window.addEventListener('load', function() {
    // Список всех твоих полей в форме
    const fields = ['cpu', 'gpu', 'motherboard', 'ram', 'powerSupply', 'case', 'storage_primary', 'storage_second', 'cooller', 'coollerCase'];

    fields.forEach(field => {
        const savedId = localStorage.getItem('build_' + field);
        const savedName = localStorage.getItem('name_' + field);

        if (savedId) {
            // 1. Возвращаем ID в скрытый select Django
            const select = document.querySelector(`select[name="${field}"]`);
            if (select) select.value = savedId;

            // 2. Возвращаем название в твой <span>
            const displayVal = document.getElementById('val-' + field);
            if (displayVal && savedName) displayVal.textContent = savedName;
        }
    });
});