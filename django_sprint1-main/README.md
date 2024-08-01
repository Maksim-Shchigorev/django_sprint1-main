# Blogicum


index.html

  <div class="container py-5">
    <article>
      <ul>    
        {% for post in posts %}
          <li>
            <h3>{{ posts.location}}</h3>
            <p>{{ posts.date }} </p>
            <li>
              Категория: <a href="{% url 'blog:posts.category' %}">{{ posts.category }}</a>
            </li>
            <p> </p>
            <p>{{ posts.text|truncatewords:10 }} </p>
              <a href="{% url 'blog:posts_detail' posts.id %}">
              Читать полный текст
              </a>  
          </li> 
          {% if not forloop.last %}
            <hr>
          {% endif %}  
        {% endfor %}  
      </ul>  
    </article>
  </div>

    <a href="{% url 'blog:posts_category' post.category %}">
                    Категория:
                    </a>  

{% extends "base.html" %}
{% block content %}
  <main>
    <div class="container py-5">
      <article>
      
         
            <h3>{{ post.location}}</h3>              
          
            <p>{{ post.date }} </p>
          
            <p>{{ post.category }} </p>
         
               
        <p>{{ post.text }} </p>      
      </article>                
    </div>
  </main>     
{% endblock %}




 <a href="{% url 'blog:category' %}">



def posts_detail(request, pk):
    # return HttpResponse(f'Публикация {pk}')
    template = 'blog/detail.html'
    context = {'post': posts[pk]}
    return render(request, template, context)

{% extends "base.html" %}
{% block content %}
  <main>
    <div class="container py-5">
      <ul>
          <li>
            <h4>Место: {{ post.location}}</h4>                
          </li>
          <li>
            <h4>Дата: {{ post.date }} </h4>
          </li>
          <li>
            <h4>Категория:</h4> <!--<a href="{% url 'blog:category' %}">not-my-day</a>-->
          </li>
      </ul>        
        <p>{{ post.text }} </p>                
                        
    </div>
  </main>
{% endblock %}




HEADER

{% load static %}
{% with request.resolver_match.view_name as view_name %}
  <header>
    <nav class="navbar navbar-light" style="background-color: lightskyblue">
      <div class="container">
        <a class="navbar-brand" href="{% url 'blog:index' %}">
          <img src="{% static 'img/logotip.png' %}"  width="30" height="30" class="d-inline-block align-top" alt="">
          Блогикум
        </a>        
        <ul class="nav  nav-pills">
          <li class="nav-item">
            <a class="nav-link {% if view_name == 'blog:index' %}active{% endif %}" href="{% url 'blog:index' %}">
              Лента записей
            </a>
          </li>
          <li class="nav-item">              
            <a class="nav-link {% if view_name == 'pages:about' %}active{% endif %}" href="{% url 'pages:about' %}">
              О проекте
            </a>
          </li>
          <li class="nav-item">  
            <a class="nav-link {% if view_name == 'pages:rules' %}active{% endif %}" href="{% url 'pages:rules' %}">
             Наши правила
            </a>
          </li>
        </ul>      
      </div>
    </nav> 
  </header>
  {% endwith %} 