from app import crear_app

# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/RayXD7/Plataforma-Educativa.git
# git push -u origin main

def funcion_principal():
    app = crear_app()
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    funcion_principal()