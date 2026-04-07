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

    if(e.target.id === 'info')
    {
       
    }
})

function sendSort(text) {
    const url = new URL(window.location.href);
    
    url.searchParams.set('category_name', text);
    
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

function openModal() {
    
}

function closeModal(modalElement) {
    modalElement.style.display = 'none';
    document.body.style.overflow = 'auto'; 
}