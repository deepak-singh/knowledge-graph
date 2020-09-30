# Knowledge graph

Points assumed for current implementation:
  - List of content already in place.
  - Content is for a Syllabus
  - Syllabus is for a subject and a standard

A content tree should be created where the concepts are linked to eachother which would help in suggesting the user with pre-requisites.

Two approaches: Nested Set or Adjacency list.

Adjacency list, although much easier to maintain, in RDBMS, will slow down the process, so I will be approaching with Nested Sets.

![](https://camo.githubusercontent.com/0a912893c429346414afdb8b380407f5927f3e30/68747470733a2f2f63646e2e7261776769742e636f6d2f7572616c626173682f73716c616c6368656d795f6d7074742f6d61737465722f646f63732f696d672f325f73716c616c6368656d795f6d7074745f74726176657273616c2e737667)


# Tools
   - Django-Tastypie
   - Django-mptt

# API Spec.
  - Creation: user should be able to send complex tree structure for a syllabus and tree should be stored. (Implemented)
  - Update: user should be able to send (patch) updates, which command the node to be moved anywhere in the current tree. (Implemented)
  - Update: user should be able to add new nodes in existing tree.    
  - Read: user should be able to retrieve tree for a syllabus. (Implemented)
  - Delete: user should be able to delete any node.
  - Read Detail: When accessing a node, api should tell us about the siblings to the left (prerequistes) 

# UI
  -  Ideal UI would be a list of all content (searchable) on the left side, from where each item can be drawn and placed on the right side for creation of tree.
    

# Implemented API:
| VERB | URL |  Details |
| ------ | ------ | ----|
| POST | /content_tree | send a Post request to content_tree with initial structure of your tree |
| PATCH | /content_tree/move_node | send a PATCH request with data: postion, node_id, target_id|
| GET | /content_tree?content__syllabus__standard=2&content__syllabus__subject=1 | Get the content tree for a syllabus |
| GET | /content_tree/:node_id | Get Tree structure with given node at root
| DELETE | Not implemented yet | |
| GET | /content/?syllabus__standard=1&syllabus__subject=2 | Get all the content for this syllabus(standard + subject)    
# To do:
    -   API to add nodes once the tree is created.
    -   API to get siblings to left of current node.
    -   API to get siblings to right of current node.
    -   API to get parent of current node.
    -   API to get only children of current node.
    -   UI: where initial creation is done by dragging the items from a different tree.



# Instructions:
  - Setup a database and change settings
  - pip install -r requirements.txt
  - python manage.py runserver (run on 8000)
  - create a super user and login to django admin and create some sample standard, subject, syllabus and content.

