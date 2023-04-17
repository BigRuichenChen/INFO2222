
<!DOCTYPE html>
  <html>
    <head>
      <style>
        .button {
          background-color: #800020;
          border: none;
          color: white;
          padding: 20px 34px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 20px;
          margin: 4px 2px;
          cursor: pointer;
        }
      </style>
    </head>
    <body>
    <p>You've chosen to chat {{friendname}}!</p>
    <p>Choose whether you like to:</p>
    <a href="/send_message" class="button">Send Message</a>
    <a href="/receive_form" class="button">Receive Message</a>
    </body>
 </html>