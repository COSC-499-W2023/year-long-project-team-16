// Placeholder user information

var user_full_name = "Andy"; // Ideally, this would come from a server or database
var user_username = "AndyUser";
var user_email = "andy@example.com";
var password = "Andy1234";
var bio = "verginia beach";

document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('name').value = user_full_name;
    document.getElementById('username').value = user_username;
    document.getElementById('email').value = user_email;
    document.getElementById('password').value = password;
    document.getElementById('bio').value = bio;
});

