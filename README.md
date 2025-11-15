#﻿# ReadMitra 📚 ****[Demo](https://youtu.be/vmbslVHMD8s?si=gZQYxmrFxXywo-Z4)****
<p>
  Welcome to <strong style="background-color: yellow; padding: 3px 5px; border-radius: 3px;">ReadMitra</strong>, a Goodreads-inspired book-tracking and review platform where users can rate, review, and organize their books into shelves. 
 <a href="https://readmitra.netlify.app/" style="margin-left: 10px;">
    <span style="text-decoration: none; color: inherit;">➡️ Visit Site!</span>
  </a></p>

## ✨ Features
### Authentication (JWT-based)
✔️ Sign-up, Sign-in, Guest User Mode.
✔️ Forgot Password via Mail OTP (Resend OTP option).
✔️ Reset Password using old password.
✔️ Email,Password validation.
✔️ Access Token to authenticate API requests.
✔️ Refresh Token to obtain a new access token.

### Books & Reviews
✔️ Admins can create books via the Django Admin Panel.
✔️ Book cover images are stored on Cloudinary and displayed on the UI.
✔️ Users can rate and review books (edit/delete their own reviews).
✔️ Book details can be viewed and edited.
### Bookshelves
✔️ Users can create bookshelves to organize their collections.
✔️ Add or remove books from bookshelves.
### Cloud Storage Integration
✔️ Utilized Cloudinary to store and retrieve book cover images dynamically
### Friend Requests & Real-Time Notifications
✔️ Users can send, accept, or reject connection requests with real-time updates via Web-Sockets. 
✔️ Notifications for friend requests and group additions are stored in the database and fetched via REST API, ensuring live updates and dynamic unread count tracking      without page refresh.
### Real-Time Chat
✔️ Developed individual & group chat functionality with Django Channels and WebSockets, supporting persistent message storage in PostgreSQL and real-time updates
  without page refresh.
### AI-Powered Quiz Generation
✔️ Integrated an AI Agent built with FastAPI that automatically generates personalized quizzes from book summaries, evaluates answers, provides scores and feedback,
  and suggests sections for review. 
✔️ When a book is added via the admin panel, a summary is generated using OpenAI API, and its embedding is stored in ChromaDB for
  Retrieval-Augmented Generation(RAG)-based quiz and feedback generation.

## 🛠️ Built with modern web technologies
### **Frontend**
- 🔹 **React.js** – For building the user interface.
- 🔹 **Redux Toolkit** – For state management.
- 🔹 **Tailwind CSS** – For responsive design and styling.
- 🔹 **Ant Design** – For UI components.
- 🔹 **React Router** – For navigation.
### **Backend**
- 🔹 **Django** – For backend development.
- 🔹 **Django REST Framework (DRF)** – For API handling.
- 🔹 **PostgreSQL** – For database management.
- 🔹 **Cloudinary** – For storing book cover images.
### **AI Agent**
- 🔹 FastAPI – Built the AI agent service for quiz generation and evaluation.
- 🔹 OpenAI API – Generated book summaries, quiz questions, and feedback.
- 🔹 ChromaDB – Stored vector embeddings for Retrieval-Augmented Generation (RAG).
- 🔹 RAG Pipeline – Used embeddings to generate context-aware quizzes and score evaluations.
- 🔹 Embeddings – Created and stored embeddings whenever a new book was added.
### **Deployment**
- 🔹 **Frontend**: Deployed on **Netlify**.
- 🔹 **Backend**: Deployed on **Render**.

 <!--
### 🚀 Upcoming Features

- 🔹 Real-time Chat for book discussions.
-->

## 📩 Contact
You can find more about me on my website: https://prachi-gore-portfolio.netlify.app/.



