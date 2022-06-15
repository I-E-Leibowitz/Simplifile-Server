package com.example.view

import com.example.Styles
import javafx.beans.InvalidationListener
import javafx.beans.Observable
import javafx.beans.property.SimpleStringProperty
import javafx.geometry.Insets
import javafx.geometry.Pos
import javafx.scene.image.Image
import javafx.scene.paint.Color
import tornadofx.*
import java.net.Socket
import java.net.ConnectException
import java.io.PrintWriter
import java.io.BufferedReader



class Login : View("Login") {
    private val usrId = SimpleStringProperty()
    private val password = SimpleStringProperty()
    private val breakValue = 0x04
    override val root = borderpane {
        paddingAll = 20
        center = form {
            hbox(alignment=Pos.CENTER) {
                fieldset("Login") {
                    addClass(Styles.sectionHeading)
                    textfield(usrId) {
                        addClass(Styles.searchLabel)
                        promptText = "Username/Email"
                    }
                    passwordfield(password) {
                        addClass(Styles.searchLabel)
                        promptText = "Password"
                    }
                }
            }
        }
        left = vbox {
            alignment = Pos.BOTTOM_LEFT
        }
        bottom = borderpane {
            left = button {
                alignment = Pos.BOTTOM_LEFT
                addClass(Styles.darkerButton)
                graphic = imageview("file:./src/main/Simplifile-Assets/general-assets/buttons-png/back.png")
                action {
                    this@Login.replaceWith(MainView::class)
                }
            }
            center = button {
                addClass(Styles.darkerButton)
                alignment = Pos.BOTTOM_CENTER
                this@button.isDefaultButton = true
                graphic = imageview("file:./src/main/Simplifile-Assets/login-screen/buttons-png/proceed.png")
                action {
                    println("USR_LOG_S")
                    validateLogin()
                    this@Login.replaceWith(StoragePage::class)
                }
            }
        }


    }
    private fun validateLogin(): Boolean {
        return try {
            val client = Socket("localhost", 55445)
            client.getOutputStream().write("command: uvalidate\nid: 5\nusername: $usrId\npassword: $password$breakValue".toByteArray())
            true
        } catch(e: ConnectException){
            println("Uh oh, something's gone wrong!")
            false
        }
    }
}