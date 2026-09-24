// Show a short message beside a field and move focus to it.
function showFieldError(field, message) {
    let error = field.parentElement.querySelector('.client-error');
    if (!error) {
        error = document.createElement('p');
        error.className = 'field-error client-error';
        error.setAttribute('role', 'alert');
        field.parentElement.appendChild(error);
    }
    error.textContent = message;
    error.hidden = false;
    field.setAttribute('aria-invalid', 'true');
    field.focus();
}

// Clear a client-side error when the user edits the field again.
document.querySelectorAll('input, textarea').forEach(function (field) {
    field.addEventListener('input', function () {
        const error = field.parentElement.querySelector('.client-error');
        if (error) error.hidden = true;
        field.setAttribute('aria-invalid', 'false');
    });
});

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function (event) {
        const firstName = document.getElementById('firstName');
        const lastName = document.getElementById('lastName');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirmPassword');
        const lettersOnly = /^\p{L}+$/u;

        if (!lettersOnly.test(firstName.value.trim())) {
            event.preventDefault();
            showFieldError(firstName, 'Use letters only for your first name.');
        } else if (!lettersOnly.test(lastName.value.trim())) {
            event.preventDefault();
            showFieldError(lastName, 'Use letters only for your last name.');
        } else if (password.value.length < 8) {
            event.preventDefault();
            showFieldError(password, 'Use at least 8 characters.');
        } else if (password.value !== confirmPassword.value) {
            event.preventDefault();
            showFieldError(confirmPassword, 'Passwords do not match.');
        }
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
        const email = document.getElementById('loginEmail');
        const password = document.getElementById('loginPassword');
        if (!email.value.trim()) {
            event.preventDefault();
            showFieldError(email, 'Enter your email address.');
        } else if (!password.value) {
            event.preventDefault();
            showFieldError(password, 'Enter your password.');
        }
    });
}

document.querySelectorAll('.comment-form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        const comment = form.querySelector('textarea[name="comment"]');
        if (!comment.value.trim()) {
            event.preventDefault();
            showFieldError(comment, 'Write a comment before posting.');
        }
    });
});

const photoInput = document.getElementById('photo');
if (photoInput) {
    const preview = document.getElementById('photoPreview');
    const dropZone = document.querySelector('.drop-zone');
    let previewUrl = null;

    photoInput.addEventListener('change', function () {
        const file = photoInput.files[0];
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        if (!file) {
            preview.hidden = true;
            dropZone.classList.remove('has-preview');
            return;
        }
        previewUrl = URL.createObjectURL(file);
        preview.src = previewUrl;
        preview.hidden = false;
        dropZone.classList.add('has-preview');
    });

    document.getElementById('uploadForm').addEventListener('submit', function (event) {
        const title = document.getElementById('title');
        const file = photoInput.files[0];
        const allowed = /\.(jpg|jpeg|png|webp)$/i;
        if (!file || !allowed.test(file.name)) {
            event.preventDefault();
            showFieldError(photoInput, 'Choose a JPG, PNG or WEBP image.');
        } else if (!title.value.trim()) {
            event.preventDefault();
            showFieldError(title, 'Give your photo a title.');
        }
    });
}

// The selected gallery view stays the same when the visitor comes back.
const gallery = document.getElementById('galleryGrid');
if (gallery) {
    const buttons = document.querySelectorAll('.view-button');
    const views = ['three', 'four', 'cards', 'list'];
    const mobileScreen = window.matchMedia('(max-width: 767px)');
    let selectedView = 'three';

    function setGalleryView(view) {
        if (!views.includes(view)) view = 'three';
        selectedView = view;
        const displayView = mobileScreen.matches
            ? (view === 'list' ? 'list' : 'cards')
            : (view === 'cards' ? 'three' : view);
        const gridClass = displayView === 'cards' ? 'three' : displayView;
        gallery.classList.remove('gallery-three', 'gallery-four', 'gallery-list');
        gallery.classList.add('gallery-' + gridClass);
        buttons.forEach(function (button) {
            const selected = button.dataset.view === displayView;
            button.classList.toggle('active', selected);
            button.setAttribute('aria-pressed', String(selected));
        });
    }

    try { setGalleryView(localStorage.getItem('galleryView')); }
    catch (error) { setGalleryView('three'); }

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            const view = button.dataset.view;
            setGalleryView(view);
            try { localStorage.setItem('galleryView', view); }
            catch (error) { /* The view still works without storage. */ }
        });
    });

    mobileScreen.addEventListener('change', function () {
        setGalleryView(selectedView);
    });
}

document.querySelectorAll('.delete-form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
        if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
});

// Replace broken image icons with a readable message.
document.querySelectorAll('.photo-image img, .detail-image img').forEach(function (image) {
    function showFallback() { image.parentElement.classList.add('image-failed'); }
    image.addEventListener('error', showFallback);
    if (image.complete && image.naturalWidth === 0) showFallback();
});

// After a server error, return focus to the first field that needs fixing.
const firstInvalidField = document.querySelector('[aria-invalid="true"]');
if (firstInvalidField) firstInvalidField.focus();
