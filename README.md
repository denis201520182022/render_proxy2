# OpenAI Proxy Service

     Прокси-сервис для [OpenAI API](https://platform.openai.com/docs/api-reference), развёртываемый на бесплатном тарифе Render.

     Принимает запросы и перенаправляет их на `api.openai.com`, подставляя ваш API-ключ.



---

     ## 🚀 Деплой на Render

     ### 1. Создайте репозиторий
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/ваш-пользователь/имя-репозитория.git
    git push -u origin main


     ### 2. Зарегистрируйтесь на Render

     Перейдите на [render.com](https://render.com) и войдите через GitHub.

     ### 3. Создайте Web Service

     1. Нажмите **New** → **Web Service**
     2. Выберите ваш репозиторий
     3. Настройте параметры:

     | Поле | Значение |
     |------|----------|
     | **Name** | `openai-proxy` (или любое другое) |
     | **Region** | Выберите любой не РФ |
     | **Branch** | `master` |
     | **Root Directory** | (пусто) |
     | **Runtime** | `Python 3` |
     | **Build Command** | `pip install -r requirements.txt` |
     | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port 8080` |
     | **Instance Type** | `Free` |

     ### 4. Добавьте Environment Variable

     В разделе **Environment**:

     | Variable | Value |
     |----------|-------|
     | `OPENAI_API_KEY` | `sk-ваш_ключ_от_openai` |

     

     ### 5. Deploy

     Нажмите **Create Web Service**. Build займёт 1-3 минуты.

     После деплоя сервис будет доступен по выданному вам уникальному адресу на ресурсе рендер
    https://ваш-сервис.onrender.com
