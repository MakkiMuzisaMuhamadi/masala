document.addEventListener('DOMContentLoaded', function() {
    const elements = document.getElementsByClassName('typewriter');
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        let texts = [];
        let currentIndex = 0;
        let index = 0;
        let isDeleting = false;
        let typingSpeed = 150;

        // Fetching texts from the database
        fetch('/get-bannertexts/')
        .then(response => response.json())
        .then(data => {
            texts = data.texts;
            typeText();
        });

        const typeText = function() {
            const currentText = texts[currentIndex];
            const nextChar = currentText.charAt(index);

            if (!isDeleting) {
                element.innerHTML = currentText.substring(0, index) + '<span class="cursor"></span>';
                index++;
                if (index <= currentText.length) {
                    setTimeout(typeText, Math.random() * typingSpeed); // Adjust the typing speed here
                } else {
                    isDeleting = true;
                    setTimeout(typeText, 1000); // Delay before starting to delete
                }
            } else {
                element.innerHTML = currentText.substring(0, index) + '<span class="cursor"></span>';
                index--;
                if (index === 0) {
                    isDeleting = false;
                    currentIndex = (currentIndex + 1) % texts.length;
                    setTimeout(typeText, 1000); // Delay before starting to type next text
                } else {
                    setTimeout(typeText, Math.random() * typingSpeed); // Adjust the typing speed here
                }
            }
        };
    }
});
