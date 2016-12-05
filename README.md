# Projectr

Projectr is a web application allowing for client-based group project courses to run more smoothly.
Potential clients can submit projects, students can bid on them, and instructors can award bids to students.

# Release Notes

### Features

#### General Features
* Students, instructors, and clients can register and passwords are stored with the Django-provided hashing mechanism.

#### Student Features
* Students can select a section to join, which will make their bids show up on their instructors dashboard.
* Students can view submitted projects and browse for interesting projects to submit bids on.
* Students can submit questions on a project that show up for the client to respond to on their dashboard, in case it is not clear
  what the student would be signing up to do if they bid on the project.
* Students can send messages to other users, in particular their instructors.
* Students will receive notifications if their bids are accepted or rejected by their instructors.

#### Instructor Features
* Instructors can send and receive messages to other users
* Instructors can see bids that have been submitted (bids include team member names and a description of why they should be awarded the project)m
  and opt to accept or reject them.
* Instructors can view projects submitted by clients and either accept them or reject them.

#### Client Features
* Clients can submit new projects, which will appear for students to bid on after an instructor approves it.
* Clients can check the status of projects they have submitted (whether they have been approved, and if so, if there are any bids on them).
* Clients can respond to questions submitted on their projects by students.



### Bug Fixes
This is release 1.0 and there have been no previous releases.



### Bugs and Defects



# Install Guide
