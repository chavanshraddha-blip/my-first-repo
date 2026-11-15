/**
 * DevLog Blogging Platform - Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize Quill Rich Text Editor if editor container is present
    const quillContainer = document.getElementById('quill-editor');
    const contentTextarea = document.getElementById('content-textarea');

    if (quillContainer && contentTextarea) {
        const quill = new Quill('#quill-editor', {
            theme: 'snow',
            placeholder: 'Write your thoughts, stories, and tutorials here...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, 4, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'color': [] }, { 'background': [] }],
                    ['link', 'image', 'clean']
                ]
            }
        });

        // Preload existing content if editing post
        if (contentTextarea.value.trim().length > 0) {
            quill.root.innerHTML = contentTextarea.value;
        }

        // On form submit, copy Quill HTML into hidden textarea
        const postForm = quillContainer.closest('form');
        if (postForm) {
            postForm.addEventListener('submit', function (e) {
                // Check if editor is practically empty (Quill leaves <p><br></p>)
                const text = quill.getText().trim();
                const html = quill.root.innerHTML;
                if (text.length === 0 && !html.includes('<img')) {
                    contentTextarea.value = '';
                } else {
                    contentTextarea.value = html;
                }
            });
        }
    }

    // 2. Auto-fade flash alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });

    // 3. Confirm Delete Prompts
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            const message = button.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});
