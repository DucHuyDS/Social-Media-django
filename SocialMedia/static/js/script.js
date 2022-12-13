$(document).ready(function () {
    refreshcontacts();
    checkerror_allauth();
    $('body').on('click','.liveToastBtn',function(){
      liveToast('Link copied');

    }) 
    $("body").on('click','button[name=like]',function (e) {
        e.preventDefault();
        var fired_button = $(this).val();
        text = $(this);
        
        $.ajax({
            url: window.location.origin+'/post/like/' + fired_button,
            method:'GET',
            success: function (data) {
              if(data.status==='anonymous'){
                alert(data.content)
            
              }
              else{
            
              
              if(data.count == 0){
                str = '<i class="fa fa-heart pe-1" ></i>Like'
              }
              else{
                str = '<i class="fa fa-heart pe-1" ></i>Like (' + data.count + ')'
              } 
                text.html(str)
                if (data.status===false) {
                  text.css('color', '');
                } else {
                  text.css('color', 'red');
                }
              }
            

            },
            error: function (data) {
                alert('This post has been deleted')
            }
        })

        
    });
    $("body").on('click','button[name=likecomment]',function (e) {
      e.preventDefault();
      var fired_button = $(this).val();
      text = $(this);
      $.ajax({
          url: window.location.origin+'/post/like_comment/' + fired_button,
          method:'GET',
          success: function (data) {
            if(data.status ==='deleted'){
              alert(data.content)
            }
            else{       
            if(data.count ==0){
              str = 'Like'
            }
            else{
              str = 'Like (' + data.count + ')'
            }       
              text.html(str)
              if (data.status===false) {
                text.css('color', '');
              } else {
                text.css('color', 'red');
              }
            }
          },
          error: function (error) {
              alert('This post has been deleted')
          }
      })

      
  });
    $("body").on('click','.friend_request',function(e){
      e.preventDefault();
      url=$(this).attr('href')
      attr=$(this).attr('data-id')
      $this=$(this)
  
        $.ajax({
          url:url,
          method:'GET',
          beforeSend: function() {
            // setting a timeout
            html=`<div class="spinner-border spinner-border-sm" role="status">
            <span class="sr-only">Loading...</span>
          </div>`           
            $this.html(html)
          },
          success: function(data){
            if(data.exist===false){
              liveToast('Sent a friend request')
              if(attr){
                btn='<i class="bi bi-person-check-fill"></i>'
              }
              else{

                btn='<a href="/profile/send_friend_request/'+data.user_id+'" class="btn btn-danger-soft me-2 friend_request"><i class="fa fa-user-minus"></i> Cancel request</a>'
              } 

            }
            else if(data.accept===true){
              if(attr){
                liveToast('Accepted')
                btn='<i class="bi bi-person-check-fill"></i>'
              }
              else{
                btn='<a class="btn btn-primary-soft me-2"  id="profileAction2" data-bs-toggle="dropdown" aria-expanded="false">\
                <i class="fa fa-user-check"></i> Friend\
              </a>\
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="profileAction2">\
                <li><a class="dropdown-item friend_request" href="/profile/remove_friend/'+data.user_id+'"> <i class="fas fa-user-times"></i> Unfriend</a></li>\
              </ul>'
              }
            }
            else{
              if(attr){
                if(attr==='accept'){
                  btn='<i class="bi bi-person-check-fill"></i>'
                }
                else{

                  btn='Add friend'
                }
              }
              else{

                btn='<a href="/profile/send_friend_request/'+data.user_id+'" class="btn btn-primary-soft me-2 friend_request"><i class="fa fa-user-plus"></i> Add friend </a>'
              }

            }

            if(attr){
              $this.html(btn)
            }
            else{
              $(`#friend_request${data.user_id}`).html(btn)
            }
          }

        })
    })  
    $('#search_contact').keyup(function(){
      $.ajax({
        type:'GET',
        url:'/profile/contact/',
        data:{
          'search_contact':$('#search_contact').val(),
          'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
        },
        success:function(data){
          document.getElementById('contacts').innerHTML=data.html
    
        }
      })
    })
    $('#noti-header').on('click',function(data){

      $.ajax({
        url:'/chat/read_noti/',
        type:'GET',
        success:function(){
          document.getElementById('icon-noti').classList.remove('badge-notif')
        }
      })
    })
    $('.emoji').on('click',function(){
      current_value=$("#chat-input").val()
      console.log(current_value)
      console.log($(this).text())
      $("#chat-input").val(current_value+$(this).text())
    })
    $("body").on("submit", ".CommentForm", function (e) {
      e.preventDefault();
      var form = $(this)
      var post_id = $(this).data('post');
      var comment_id = $(this).data('parent');
      var url = $(this).data('url');
      data=form.serializeArray()
      data.push({
        name:'csrfmiddlewaretoken',value:$('input[name=csrfmiddlewaretoken]').val()
      })   
      $.ajax({
          method: 'POST',
          url: url,
          data: $.param(data),
          dataType: 'json',
          success: function (data) {
            if(data.status==='deleted'){
              alert(data.content)
            }
            else{

            
              form[0].reset();
              html = '\
        <li id="'+data.comment_id+'" class="comment-item">\
        <div class="d-flex">\
          <div class="avatar avatar-xs">\
            <a href="#"> <img class="avatar-img rounded-circle" src="' + data.img + '"\
                alt=""> </a>\
          </div>\
          <div class="ms-2" style="width:100%">\
            <div class="bg-light rounded-start-top-0 p-3 rounded" >\
              <div class="d-flex justify-content-between">\
                <h6 class="mb-1"> <a href="#!"> ' + data.first_name + ' ' + data.last_name + '</a></h6>\
                <small class="ms-2">Just now</small>\
              </div>\
              <p class="small mb-0">' + data.content + '</p>\
            </div>\
            <ul class="nav nav-divider py-2 small">\
              <li class="nav-item">\
                <button class="nav-link" name="likecomment" value="'+data.comment_id+'" style="border:none;background-color:white;color:" > Like</button>\                </li>\
              <li class="nav-item ">\
                <a class="nav-link" id="reply" role="button" data-bs-toggle="dropdown" aria-expanded="false"\
                  data-bs-auto-close="outside">\
                  Reply\
                </a>\
                <div class="dropdown-menu dropdown-animation dropdown-menu-start dropdown-menu-size-md p-0 shadow-lg border-0"\
                  aria-labelledby="reply">\
                  <form class="CommentForm Reply" data-url="' + url + '" method="POST" data-post="' + post_id + '" data-parent="' + data.comment_id + '">\
                    <input class="form-control pe-4 " rows="1" placeholder="Reply..." name="commentparent" required>\
                    <input class="form-control pe-4 " type="hidden" name="comment" value="' + data.comment_id + '">\
                  </form>\
                </div>\
              </li>\
              <li class="dropdown nav-item">\
                <a href="#" class="text-secondary py-1 px-2" id="cardFeedAction"\
                  data-bs-toggle="dropdown" aria-expanded="false">\
                  <i class="bi bi-three-dots"></i>\
                </a>\
                <!-- Card feed action dropdown menu -->\
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="cardFeedAction">\
                  <li><a class="dropdown-item" onclick="confirm('+"'Are you sure'"+')&& delete_comment('+data.comment_id+')" style="cursor: pointer;"> <i class="bi bi-x-circle fa-fw pe-2"></i>Delete</a></li>\
                </ul>\
              </li>\
            </ul>\
          </div>\
        </div>\
        <ul class="comment-wrap list-unstyled">\
          <li class="comment-item">\
            <ul class="commentchild' + data.comment_id + ' comment-item-nested list-unstyled" name="{{comment.id}}">\
            </ul>\
          </li>\
        </ul>\
      </li>';
              html2 = '\
      <li id="'+data.comment_id+'" class="comment-item">\
                        <div class="d-flex">\
                          <!-- Avatar -->\
                          <div class="avatar avatar-xs">\
                            <a href="#!"><img class="avatar-img rounded-circle" src="' + data.img + '"\
                                alt=""></a>\
                          </div>\
                          <!-- Comment by -->\
                          <div class="ms-2" style="width: 100%">\
                            <div class="bg-light p-3 rounded">\
                              <div class="d-flex justify-content-between">\
                                <h6 class="mb-1"> <a href="#!"> ' + data.first_name + ' ' + data.last_name + '</a>\
                                </h6>\
                                <small class="ms-2">Just now</small>\
                              </div>\
                              <p class="small mb-0">' + data.content + '</p>\
                            </div>\
                            <!-- Comment react -->\
                            <ul class="nav nav-divider py-2 small">\
                              <li class="nav-item">\
                              <button class="nav-link" name="likecomment" value="'+data.comment_id+'" style="border:none;background-color:white;" > Like</button>\                                </li>\
                              <li class="nav-item ">\
                                <a class="nav-link" id="reply" role="button" data-bs-toggle="dropdown" aria-expanded="false"\
                                  data-bs-auto-close="outside">\
                                  Reply\
                                </a>\
                                <div class="dropdown-menu dropdown-animation dropdown-menu-start dropdown-menu-size-md p-0 shadow-lg border-0"\
                                  aria-labelledby="reply">\
                                  <form class="CommentForm Reply" data-url="' + url + '" " method="POST"\
                                    data-post="' + post_id + '" data-parent="' + comment_id + '">\
                                    <input class="form-control pe-4 " rows="1" placeholder="Reply..." name="commentparent" required>\
                                    <input class="form-control pe-4 " type="hidden" name="comment" value="' + comment_id + '">\
                                  </form>\
                                </div>\
                              </li>\
                              <li class="dropdown nav-item">\
                        <a href="#" class="text-secondary py-1 px-2" id="cardFeedAction"\
                          data-bs-toggle="dropdown" aria-expanded="false">\
                          <i class="bi bi-three-dots"></i>\
                        </a>\
                        <!-- Card feed action dropdown menu -->\
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="cardFeedAction">\
                          <li><a class="dropdown-item" onclick="confirm('+"'Are you sure'"+')&& delete_comment('+data.comment_id+')" style="cursor: pointer;"> <i class="bi bi-x-circle fa-fw pe-2"></i>Delete</a></li>\
                \
                        </ul>\
                      </li>\
                            </ul>\
                          </div>\
                        </div>\
                      </li>';

              if (form.attr('class') == 'CommentForm Reply') {
                  $('.commentchild' + form.data('parent')).append(html2)
                  $('#comment_count'+post_id).html('<i  class=" fa fa-comment-o pe-1"></i>Comments ('+data.comments+')')
              } else {
                  $('.comment-wrap' + post_id).prepend(html)
                  $('#comment_count'+post_id).html('<i  class=" fa fa-comment-o pe-1"></i>Comments ('+data.comments+')')

              }
              $('#comment' + post_id).html('<i class="fa fa-comment-o pe-1"></i>Comments (' + data.comments + ')')
            }
            },
          error: function(err){
            alert('This post has been deleted')
          }
      })
    })
  
  })
function showcomment(post_id){
  var x = document.getElementById(post_id)
  if(x.style.display==='none'){
      x.style.display='block';
  }
  else{
    x.style.display='none';
  }
  
}
function delete_post(post_id){
  $.ajax({
    url:window.location.origin+'/post/delete_post/'+post_id,
    success: function(){
      $('#'+post_id).fadeOut('slow')
      liveToast('Deleted')
      
    }
  })
}
function delete_comment(comment_id){
  var div = document.getElementById(comment_id)
  $.ajax({
    url:window.location.origin+'/post/delete_comment/'+comment_id,
    success: function(data){
      div.remove()
      html='<i  class=" fa fa-comment-o pe-1"></i>Comments ('+data.comments+')'
      $('#comment_count'+data.post_id).html(html)
      
    }
  })
}

function delete_friend(friend_id){
  $.ajax({
    url:window.location.origin+'/profile/remove_friend/'+friend_id,
    success: function(){
      $('.friend'+friend_id).fadeOut('slow', function(){ 
        $(this).remove();
      });
      liveToast('Deleted')
      
    }
  })
}


setTimeout(function () {
  $('#messages').fadeOut('slow')
}, 4000);
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function refreshcontacts(){
  
  setTimeout(refreshcontacts, 60000);
  $.ajax({
    url:'/profile/contact/',
    type:'GET',
    success: function(data){
      document.getElementById('contacts').innerHTML=data.html
    }
  })

}


function liveToast(str){
  html=`<div class="toast-body"><i class="fa fa-check" style="color:green"></i> ${str}</div>`
  var toastLiveExample = document.getElementById('liveToast')
  toastLiveExample.innerHTML=html
  var toast = new bootstrap.Toast(toastLiveExample)
  toast.show()
}

function checkerror_allauth(){
  var errors = document.querySelectorAll("ul.errorlist")

  for (var i = 0; i < errors.length; i++) {
    errors[i].style.color = "red";
    errors[i].id='messages'
  }

}