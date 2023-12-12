async function likePost(likeBtn, e) {
    e.preventDefault()
    console.log('liking post id ' + likeBtn.dataset.postid, likeBtn.dataset.liker)
    await fetch("like", {
        method: "POST",
        body: JSON.stringify({
            postID: likeBtn.dataset.postid,
            liker: likeBtn.dataset.liker
        })
    }).then(response => response.json()).then(result => console.log(result))

    likeBox = likeBtn.parentNode;
    console.log(likeBox)
    likeCount = likeBox.querySelector('.like_count')
    console.log(likeCount)
    likeCount.textContent = Number(likeCount.textContent) + 1
}