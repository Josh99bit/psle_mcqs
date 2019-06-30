// when the webpage is loaded
$(document).ready(function(){

  $("form#attempt_question").on( "submit",  function(e){ 
    e.preventDefault()
    given_answer = parseInt($(this).find("input:checked").val())
    qid = $(this).data("qid")
    given_params = {
      "given_answer": given_answer
    }

    // 1. disables buttons
    $("form button").attr("disabled",  true)

    axios.post('/questions/'+qid+'/attempt', null, { 
        params: given_params
      })
      .then(function (response) { 
        if (response.data.correct) {
          $(".completed_container .message").text("Correct")
        } else {
          $(".completed_container .message").text("Wrong! Right answer is "+response.data.answer)
        }
        $(".completed_container").toggle()
      })
      .catch(function (error) {
        alert("Something went wrong!\n" + error)
        $("form button").attr("disabled",  false)
      });    
  })

  // when the form 
  $("form#register").on( "submit",  function(e){ 
      // prevents page from reloading
      e.preventDefault(); 

      name = $(this).find("input#name").val()
      email = $(this).find("input#email").val()
      password = $(this).find("input#password").val()

      // do not do the post request if any of these is missing
      if (isEmpty(name) || isEmpty(email) || isEmpty(password) ) {
        alert ("All the fields are required")
        return
      }

      // the parameters needed for the post request
      given_params = {
        name: name,
        email: email,
        password: password
      }

      // makes a POST request to register. third param is to submit as params
      axios.post('/register', null, { 
          params: given_params
        })
        .then(function (response) {
          alert ("Successfully Registered!")
          window.location.href="/get_new_question"
        })
        .catch(function (error) {
          // SHOULD SHOW THE RIGHT ERROR
          alert ("Oops, something went wrong. Maybe email is already taken?")
        });    
    }
  )

  $("form#login").on("submit", function(e){
    e.preventDefault()
    email = $(this).find("input#email").val()
    password = $(this).find("input#password").val()

    // if any field is empty, do not sumit
    if (isEmpty(email) || isEmpty(password) ) {
      alert ("All the fields are required")
      return
    }

    params = {
      email: email, 
      password: password
    }

    axios.post("/login", null, {params: params})
      .then(function(response){
        alert ("Logined successfully")
        window.location.href="/get_new_question"
      })
      .catch(function(error){
        alert(error)
      })

  })

});

// helper function to 
function isEmpty(str) {
  return str == null || str == ""
}

function showCorrectAnswer(correct, given_answer, answer) {
  if (correct){
    
  } else {
    
  }
}
