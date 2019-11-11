
### Project name: Garifeld C.L.I Todo
##### Developed by: Garfield with <3



### Objectives 🥇

Learn how to pass and consume arguments from the command line.

Learn how to access a SQL database from our Python applications.

Learn how to use the SQLite3 plugin for VScode.

Learn how to use Fire to C.R.U.D. our resources.

### Required Features 🎯

- [x] User can see all todos from the command line by passing a list command, sorted by due todos first.

- [x] User can add a todo from the command line by passing an argument, add. The fields specified should be body, due_date, and project_id. The fields due_date and project_id are optional. Only body is required.

- [X] By default todos are incomplete.

- [x] User should see a message giving information about the todo that was added.

- [x] User can mark a todo as complete by passing a command and an id.

- [x] User can mark a todo as incomplete by passing a command and an id.

- [x] If the user does not supply the correct arguments, or supplies a --help flag, the user sees a usage message.

- [x] The user can supply arguments to the list command to only see todos that are complete.

- [x] Project has a ERD Diagram in it's README.md.

### Rockets 🚀

- [x] User can use the app as a R.E.P.L.

- [x] User can supply arguments to the list command to only see todos of a particular project_id.

- [ ] User can supply arguments to the list command to reverse the default sort, to now see the todos by due_date descending.

- [x] User can supply arguments to the list command to combine the above options.

- [x] User can add a user_id to each todo.

- [x] User can add a user to the system by passing add_user. Each user should have a name, email_address, and id.

- [x] User can call a list_users command that shows all the users in the system.

- [x] User can call a staff command that shows each project, combined with each of the users working on that project.

- [x] User can call a who_to_fire command that lists all users who are not currently assigned a todo.

- [x] User can add a project by calling add_project. Each project must have a name.

- [x] User can see all projects from the command line.

### Command list

==========================================================  ==========================
-h, --help                                                  show this message
-list, --list "custom status" "custom_id"                   show Todo list.
-add, --add "TODO CONTENT" "PROJECT ID"                     add Todo to Todo list.
-del, --del "Todo ID"                                       remove todo from todo list
-mod, --mod "Todo ID" "status"                              modify todo status
-create, --create "Project Name"                            create a new project
-assignTo, --assignTo "Todo ID" "USER ID"                   assign a Todo to a user
-userList, --userList                                       See current user list
-projectList, --projectList                                 See current Project list
-assignToProject, --assignToProject "USER ID" "PROJECT ID"  Add a user to project
-who_to_fire, --who_to_fire                                 Show a list of lazy users!
==========================================================  ==========================


