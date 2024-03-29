function follow(accountID){
    $('#follow' + accountID).hide();
    $('#unfollow' + accountID).show();

    $.ajax(
    {
        type:"GET",
        url: location.origin + '/user/follow_toggle',
        data:{
            user_id: accountID,
            request_type: 'follow'
        },
        success: function(data){
        }
    })
    
    try{
        accounts_slider.logged_user_following_ids.add(parseInt(accountID));
    }catch(err){}
}

function unfollow(accountID){
    $('#unfollow' + accountID).hide();
    $('#follow' + accountID).show();

    $.ajax(
    {
        type: "GET",
        url: location.origin + '/user/follow_toggle',
        data:{
            user_id: accountID,
            request_type: 'unfollow'
        },
        success: function(data){
        }
    })

    try{
        accounts_slider.logged_user_following_ids.remove(parseInt(accountID));
    }catch(err){}
}

function like_post(postID){
    var element = document.querySelector('#lb'+postID);
    var old_likes_str = document.getElementById("number_of_likes" + postID).innerHTML.trim();
    var new_likes = parseInt(old_likes_str.split(" ")[0]);

    if(element.classList.contains('fa')){
        new_likes -= 1;
        element.classList.remove('fa');
        element.classList.add('far');
    }
    else{
        new_likes += 1;
        element.classList.remove('far');
        element.classList.add('fa');
    }

    if (new_likes == 1){
        new_likes = '1 like';
    }else{
        new_likes = new_likes + ' likes';
    }
    document.getElementById('number_of_likes'+postID).innerHTML = new_likes;

    $.ajax({
        type:"GET",
        url: location.origin + '/user/like',
        data:{
            post_id: postID
        },
        success: function(data){}
    })
}

function load_comment(userID, postID){
    if ($('#comment-box-wrapper'+postID).is(":visible")){
        $('#comment-box-wrapper'+postID).slideUp();
    }else{
        $.ajax({
            type: "GET", 
            url: location.origin + '/user/loadComments',
            data: {
                postID: postID
            },
            success: function(data){
                var comments = JSON.parse(data);
                var new_inner_html = '';

                for (var comment in comments){
                    var heart_type = 'far';
                    var liked_by = new Set(comments[comment].liked_by);
                    if (liked_by.has(userID)){
                        heart_type = 'fa';
                    }

                    var comment_likes = '';
                    if (comments[comment].total_likes == 1){
                        comment_likes = '1 like';
                    }else{
                        comment_likes = comments[comment].total_likes + ' likes';
                    }
                    
                    new_inner_html +=
                    ('<div class="comment">'+
                        '<img src="' + comments[comment].user_details.avatar_url + '" alt="Error!" style="border: 1.5px rgb(240, 240, 240) solid; border-radius: 20px; margin-right: 10px" height="40px" width="40px">' +
                        '<div style="line-height: 120%; margin-right: 20px; width: 100%;">' +
                            '<span style="font-weight: 650;">' + comments[comment].user.username + ' </span>' +
                            '<span>' + comments[comment].text + '</span>' + 
                            '<div class="comment-info">' + 
                                '<span class="comment-time-elapsed">' + comments[comment].time_elapsed + '</span>' + 
                                '<span class="comment-likes" id="cmtlikes' + comments[comment].id + '">' + comment_likes + '</span>' +
                            '</div>' +
                        '</div>' +
                        '<button class="' + heart_type + ' fa-heart post-interaction-button" onclick="like_comment(commentID = ' + comments[comment].id + ')" id="clb' + comments[comment].id + '" href="#" style="font-size: 1em;"></button>' +
                    '</div>');
                }
                document.getElementById('comments-layout'+postID).innerHTML = new_inner_html;
                $('#comment-box-wrapper'+postID).slideDown();
                document.getElementById('comment-box-wrapper'+postID).style.display = 'flex';
            }
        })
    }
}

function like_comment(commentID){
    $.ajax({
        type: 'GET',
        url: location.origin + '/user/likeComment',
        data: {
            commentID: commentID
        },
        success: function(data){
            var context = JSON.parse(data);
            var comment_likes = '';
            var comment_like_button = document.querySelector('#clb'+commentID);
            if (context.total_likes == 1){
                comment_likes = '1 like';
            }else{
                comment_likes = context.total_likes+' likes';
            }
            document.getElementById('cmtlikes'+commentID).innerHTML = comment_likes;

            if (context.action == 'liked'){
                comment_like_button.classList.remove('far');
                comment_like_button.classList.add('fa');
            }else{
                comment_like_button.classList.remove('fa');
                comment_like_button.classList.add('far');
            }
        }
    })
}