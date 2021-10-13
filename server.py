from flask import Flask, session, render_template, redirect, request, flash
from cardealz_app import app
from cardealz_app.controllers import cars_controller, users_controller


if __name__ == '__main__':
    app.run(debug=True)