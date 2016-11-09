on send_imessage(first_name, last_name, phone_number, message)
  
  tell application "Messages"
      set targetService to 1st service whose service type = iMessage
      set targetBuddy to buddy phone_number of targetService
      
      try
        send message to targetBuddy
      on error
        create_contact(first_name, last_name, phone_number)
      end try

  end tell

end send_imessage


on create_contact(first_name, last_name, phone_number)
  tell application "Address Book"

    set thePerson to make new person with properties ¬
      {first name: first_name, last name: last_name, ¬
      organization:""}

    make new phone at end of phones of thePerson with properties ¬
      {label:"Work", value:phone_number}

    save

  end tell
end create_contact


on delete_contact(phone_number)
  tell application "Address Book"
    
    set contactList to people whose (value of phones contains phone_number)
    repeat with contact in contactList
      delete contact
    end repeat
    save

  end tell
end delete_contact

