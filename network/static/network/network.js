async function likePost(likeBtn, e) {
    e.preventDefault()
    await fetch("like", {
        method: "POST",
        body: JSON.stringify({
            operation: "like",
            postID: likeBtn.dataset.postid,
            liker: likeBtn.dataset.liker
        })
    }).then(response => response.json()).then(result => {
        console.log(result)
        likeBox = likeBtn.parentNode;
        likeCount = likeBox.querySelector('.like_count')
        likeCount.textContent = Number(likeCount.textContent) + 1
        likeBtn.textContent = 'Unlike'
        likeBtn.setAttribute('onclick', 'unLikePost(this, event)')
    })
}

async function unLikePost(unLikeBtn, e) {
    e.preventDefault()
    await fetch("like", {
        method: "POST",
        body: JSON.stringify({
            operation: "unlike",
            postID: unLikeBtn.dataset.postid,
            liker: unLikeBtn.dataset.liker
        })
    }).then(response => response.json()).then(result => {
            console.log(result)
            likeBox = unLikeBtn.parentNode;
            likeCount = likeBox.querySelector('.like_count')
            likeCount.textContent = Number(likeCount.textContent) - 1
            unLikeBtn.textContent = 'Like'
            unLikeBtn.setAttribute('onclick', 'likePost(this, event)')
    })
}