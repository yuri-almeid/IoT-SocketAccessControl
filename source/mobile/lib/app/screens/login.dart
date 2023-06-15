import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mobile/app/core/api.dart';
import 'package:mobile/app/core/colors.dart';
import 'package:mobile/app/screens/home.dart';
import 'package:mobile/app/screens/register.dart';
import 'package:mobile/app/widgets/custom_input.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  bool loading = false;
  bool recoveryLoading = false;
  String errorText = ' ';

  @override
  Widget build(BuildContext context) {
    final baseUrl = Urls.baseUrl;

    double screenSize = MediaQuery.of(context).size.height;
    double screenWidth = MediaQuery.of(context).size.width;

    double forgotPasswordModalSize = 350;

    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
        width: double.infinity,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                height: screenSize * .07,
              ),
              Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 50,
                    vertical: 150,
                  ),
                  child: Image.asset(
                    "assets/images/minorLogo.png",
                    height: 140,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 30),
                child: Column(
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    TextFormField(
                      controller: _emailController,
                      decoration: customTextFieldDecoration(
                        hintText: 'E-mail',
                      ),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    TextFormField(
                      controller: _passwordController,
                      decoration: customTextFieldDecoration(
                        hintText: 'Senha',
                      ),
                      obscureText: true,
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    Material(
                      color: AppColors.primaryColor,
                      borderRadius: BorderRadius.circular(50),
                      child: InkWell(
                        onTap: () async {
                          SharedPreferences prefs =
                              await SharedPreferences.getInstance();

                          setState(() {
                            loading = true;
                          });
                          if (_emailController.text.isEmpty ||
                              _passwordController.text.isEmpty) {
                            setState(() {
                              errorText = 'Preencha todos os campos';
                            });
                            setState(() {
                              loading = false;
                            });
                            return;
                          }
                          final url = Uri.parse("${Urls.baseUrl}/login");
                          var data = {
                            'email': _emailController.text,
                            'password': _passwordController.text,
                          };
                          var body = jsonEncode(data);
                          var headers = {'Content-Type': 'application/json'};

                          var response = await http.post(url,
                              headers: headers, body: body);
                          setState(() {
                            loading = false;
                          });
                          if (response.statusCode == 200) {
                            prefs.setString(
                              "email",
                              _emailController.text,
                            );
                            prefs.setString(
                              "password",
                              _passwordController.text,
                            );
                            Navigator.of(context).pushReplacement(
                              MaterialPageRoute(
                                builder: (context) => MyHomePage(
                                  title: "Home",
                                ),
                              ),
                            );
                          } else {
                            setState(() {
                              errorText = 'E-mail ou senha incorretos';
                            });
                          }
                        },
                        borderRadius: BorderRadius.circular(50),
                        child: Container(
                          width: screenWidth - 60,
                          height: 49,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                          ),
                          alignment: Alignment.center,
                          child: (loading)
                              ? const Padding(
                                  padding: EdgeInsets.all(8.0),
                                  child: CircularProgressIndicator(
                                    color: Colors.white,
                                  ),
                                )
                              : const Text(
                                  'Entre',
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontFamily: 'outline',
                                    fontWeight: FontWeight.w500,
                                    color: Colors.white,
                                  ),
                                ),
                        ),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(top: 10),
                      child: Text(
                        errorText,
                        style: const TextStyle(
                          color: Colors.red,
                          fontFamily: 'outfit',
                          fontWeight: FontWeight.w400,
                          fontSize: 16,
                        ),
                      ),
                    ),
                    SizedBox(
                      height: screenSize * .1,
                    ),
                    const Text(
                      'Você ainda não tem conta?',
                      style: TextStyle(
                        fontFamily: 'outfit',
                        fontWeight: FontWeight.w400,
                        fontSize: 16,
                      ),
                    ),
                    InkWell(
                      onTap: () {
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(
                            builder: (context) => RegisterScreen(),
                          ),
                        );
                      },
                      child: const Text(
                        'Registre agora',
                        style: TextStyle(
                          fontFamily: 'outfit',
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                    )
                  ],
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
