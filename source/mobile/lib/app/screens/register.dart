import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mobile/app/core/api.dart';
import 'package:mobile/app/core/colors.dart';
import 'package:mobile/app/screens/home.dart';
import 'package:mobile/app/screens/login.dart';
import 'package:mobile/app/widgets/custom_text_field.dart';
import 'package:mobile/app/widgets/sign_subtitle_style.dart';
import 'package:mobile/app/widgets/sign_title_style.dart';
import 'package:mask_text_input_formatter/mask_text_input_formatter.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final baseUrl = Urls.baseUrl;

  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  TextEditingController _firstNameController = TextEditingController();
  TextEditingController _lastNameController = TextEditingController();
  TextEditingController _phoneController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    double screenSize = MediaQuery.of(context).size.height;
    double screenWidth = MediaQuery.of(context).size.width;

    final phoneMaskFormatter = MaskTextInputFormatter(mask: '(##) #####-####');

    return Scaffold(
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
              Padding(
                padding: const EdgeInsets.only(left: 18),
                child: Text(
                  'Registre sua \nconta',
                  style: signTitleStyle(),
                ),
              ),
              const SizedBox(
                height: 8,
              ),
              Padding(
                padding: const EdgeInsets.only(left: 18),
                child: Text(
                  'Espero que tenha \nboas compras',
                  style: signSubtitleStyle(),
                ),
              ),
              const SizedBox(
                height: 24,
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 23),
                child: Column(
                  mainAxisSize: MainAxisSize.max,
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    TextField(
                      controller: _firstNameController,
                      textInputAction: TextInputAction.next,
                      decoration: customTextFieldDecoration(hintText: 'Nome'),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    TextField(
                      textInputAction: TextInputAction.next,
                      controller: _lastNameController,
                      decoration:
                          customTextFieldDecoration(hintText: 'Sobrenome'),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    TextField(
                      textInputAction: TextInputAction.next,
                      controller: _phoneController,
                      keyboardType: TextInputType.phone,
                      inputFormatters: [phoneMaskFormatter],
                      decoration:
                          customTextFieldDecoration(hintText: 'Telefone'),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    TextField(
                      textInputAction: TextInputAction.next,
                      controller: _emailController,
                      decoration: customTextFieldDecoration(hintText: 'Email'),
                      keyboardType: TextInputType.emailAddress,
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    TextField(
                      textInputAction: TextInputAction.done,
                      controller: _passwordController,
                      decoration: customTextFieldDecoration(hintText: 'Senha'),
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
                          bool isNotEmpty = (_emailController.text.isNotEmpty &&
                              _firstNameController.text.isNotEmpty &&
                              _lastNameController.text.isNotEmpty &&
                              _phoneController.text.isNotEmpty &&
                              _passwordController.text.isNotEmpty);

                          if (isNotEmpty) {
                            var url = Uri.parse('$baseUrl/register');
                            var data = {
                              'email': _emailController.text,
                              'password': _passwordController.text,
                              'first_name': _firstNameController.text,
                              'last_name': _lastNameController.text,
                              'phone_number': _phoneController.text,
                            };
                            var body = jsonEncode(data);
                            var headers = {'Content-Type': 'application/json'};

                            var response = await http.post(url,
                                headers: headers, body: body);
                            if (response.statusCode == 201) {
                              SharedPreferences prefs =
                                  await SharedPreferences.getInstance();
                              prefs.setString(
                                'email',
                                _emailController.text,
                              );
                              prefs.setString(
                                'password',
                                _passwordController.text,
                              );

                              Navigator.of(context).pushReplacement(
                                MaterialPageRoute(
                                  builder: (context) => const MyHomePage(
                                    title: "Home",
                                  ),
                                ),
                              );
                            } else {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content:
                                      Center(child: Text('Erro ao registrar')),
                                ),
                              );
                            }
                          }
                        },
                        borderRadius: BorderRadius.circular(50),
                        child: Container(
                          width: screenWidth - 46,
                          height: 49,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                          ),
                          alignment: Alignment.center,
                          child: const Text(
                            'Registrar',
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
                    SizedBox(
                      height: screenSize * .1,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text(
                          'Você já possui uma conta?',
                          style: TextStyle(
                            color: Colors.black,
                            fontFamily: 'outfit',
                            fontSize: 16,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                        InkWell(
                          onTap: () {
                            Navigator.of(context).pushReplacement(
                                MaterialPageRoute(
                                    builder: (context) => const LoginScreen()));
                          },
                          child: const Text(
                            ' Entre',
                            style: TextStyle(
                              color: Colors.black,
                              fontFamily: 'outfit',
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        )
                      ],
                    )
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
