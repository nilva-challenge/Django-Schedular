# Django Task Scheduler Project

## Introduction
This Django project is designed to manage and schedule tasks for users, with a focus on providing a robust and scalable API. Key features include task creation, update, deletion, and scheduling tasks to send email reminders using Celery.

## Initial Setup and Planning
- **Project Initiation**: The project commenced with the goal of creating an efficient task management system using Django and Django REST Framework.
- **Requirements Gathering**: Functional requirements were identified, including user authentication, task management, and scheduled notifications.
- **Planning Tools**: Utilized Trello for task tracking and breakdown, ensuring organized and phased development.

## Development Phases

### Phase 1: Project Setup
- **Setting Up the Development Environment**: Configured a virtual environment, installed Django and necessary dependencies.
- **Version Control Setup**: Initialized a Git repository with Git Flow, establishing a systematic branching strategy for features, releases, and hotfixes.

### Phase 2: Core Feature Implementation
- **Building the Models**: Developed a `CustomUser` model extending `AbstractUser` and a `Task` model with fields for title, description, owner, schedule time, and pre-tasks.
- **Creating Views and Serializers**: Implemented API views using `APIView` for handling CRUD operations and serializers for data validation and serialization.
- **Integrating Celery for Task Scheduling**: Set up Celery with Redis as the broker to handle asynchronous task scheduling for email notifications.

### Phase 3: Testing and Refinement
- **Writing Unit Tests**: Comprehensive tests written for models, views, and serializers to ensure reliability and correctness.
- **Refactoring and Code Review**: Code was continuously refactored and reviewed for optimization and adherence to best practices.

### Phase 4: Additional Features and Enhancements
- **Implementing Additional Features**: Added advanced features like email notifications using Celery.
- **Optimizations**: Performed query optimizations and code enhancements for better performance.

## Challenges and Solutions
- Faced challenges in Celery integration for task scheduling, which were resolved through meticulous testing and configuration adjustments.
- Overcame complexities in handling user permissions and task dependencies.

## Conclusion and Reflection
This project was a comprehensive exercise in building a full-featured Django application with RESTful APIs, background task processing, and unit testing. Key learnings include effective Django project structuring, advanced model relationships, and asynchronous task scheduling with Celery.
