function scrollSlider(distance) {
    const slider = document.getElementById('slider');
    if (slider) {
        slider.scrollBy({
            left: distance,
            behavior: 'smooth'
        });
    }
}