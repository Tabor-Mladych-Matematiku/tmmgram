const postsContainer = document.getElementById('posts');
const statusElement = document.getElementById('posts-status');
const sentinel = document.getElementById('posts-sentinel');
const limit = parseInt(postsContainer?.dataset?.limit || '10', 10);
const postsUrl = postsContainer?.dataset?.postsUrl || '/posts';

if (!postsContainer || !statusElement || !sentinel) {
    throw new Error('Missing infinite scroll elements');
}

let isLoading = false;
let hasMore = true;

function applyLikeUi(button, liked, likesCount) {
    const icon = button.querySelector('i');
    if (icon) {
        icon.classList.toggle('bi-heart-fill', liked);
        icon.classList.toggle('text-danger', liked);
        icon.classList.toggle('bi-heart', !liked);
    }
    button.dataset.liked = liked ? 'true' : 'false';

    const postId = button.dataset.postId;
    const countElement = postsContainer.querySelector(`.post-like-count[data-post-id="${postId}"]`);
    if (countElement) {
        countElement.textContent = String(likesCount);
    }
}

function setStatus(text) {
    statusElement.textContent = text;
    statusElement.style.display = text ? 'block' : 'none';
}

async function loadMorePosts() {
    if (isLoading || !hasMore) {
        return;
    }

    isLoading = true;
    setStatus('Načítání...');

    try {
        const offset = postsContainer.querySelectorAll('article').length;
        const response = await fetch(`${postsUrl}?limit=${limit}&offset=${offset}`);
        const html = await response.text();

        if (html.trim().length === 0) {
            hasMore = false;
            setStatus('Žádné další příspěvky');
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.innerHTML = html;

        while (wrapper.firstChild) {
            postsContainer.appendChild(wrapper.firstChild);
        }

        setStatus('');
    } catch (error) {
        setStatus('Nepodařilo se načíst další příspěvky');
    } finally {
        isLoading = false;
    }
}

const observer = new IntersectionObserver((entries) => {
    if (entries.some(entry => entry.isIntersecting)) {
        loadMorePosts();
    }
});

observer.observe(sentinel);

postsContainer.addEventListener('click', async (event) => {
    const button = event.target.closest('.post-like-button');
    if (!button || button.disabled) {
        return;
    }

    const postId = button.dataset.postId;
    if (!postId) {
        return;
    }

    button.disabled = true;

    try {
        const response = await fetch(`/posts/${postId}/like-toggle`, {
            method: 'POST'
        });

        if (!response.ok) {
            console.error('Like toggle failed:', (await response.json()).error);
        }

        const payload = await response.json();
        applyLikeUi(button, !!payload.liked, Number(payload.likes_count || 0));
    } catch (error) {
        console.error('Like toggle failed:', error);
    } finally {
        button.disabled = false;
    }
});