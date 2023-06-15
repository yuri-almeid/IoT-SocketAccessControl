import 'dart:convert';

import 'package:dropdown_button2/custom_dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:mobile/app/core/api.dart';
import 'package:mobile/app/core/colors.dart';
import 'package:mobile/app/screens/login.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final baseUrl = Urls.baseUrl;
  final urlStores = Uri.parse("${Urls.baseUrl}/stores");

  Future<List<String>> getStores() async {
    final response = await http.get(urlStores);
    final List<dynamic> stores = json.decode(response.body);
    final List<String> storeNames = [];

    for (var store in stores) {
      storeNames.add(store['name']);
    }

    return storeNames;
  }

  @override
  void initState() {
    super.initState();
    getStores().then((storeNames) {
      setState(() {
        items = storeNames;
      });
    });
  }

  List<String> items = [];
  String? selectedValue;
  bool loading = false;

  @override
  Widget build(BuildContext context) {
    double screenSize = MediaQuery.of(context).size.height;
    double screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
        width: double.infinity,
        child: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 130,
              width: double.infinity,
              decoration: BoxDecoration(
                color: AppColors.primaryColor,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(30),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.5),
                    spreadRadius: 5,
                    blurRadius: 7,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const SizedBox(
                      height: 40,
                    ),
                    Image.asset(
                      "assets/images/namedLogo.png",
                      height: 25,
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(30),
              child: Container(
                height: 400,
                width: 400,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.black),
                  borderRadius: const BorderRadius.all(
                    Radius.circular(30),
                  ),
                ),
                child: const Center(
                  child: Text('<Mapa>'),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 35),
              child: CustomDropdownButton2(
                dropdownWidth: 350,
                buttonWidth: double.infinity,
                hint: 'Selecione uma loja',
                dropdownItems: items,
                value: selectedValue,
                onChanged: (value) {
                  setState(() {
                    selectedValue = value;
                  });
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(30),
              child: Material(
                color: AppColors.primaryColor,
                borderRadius: BorderRadius.circular(50),
                child: InkWell(
                  onTap: () async {
                    SharedPreferences prefs =
                        await SharedPreferences.getInstance();
                    final urlStore =
                        Uri.parse("${Urls.baseUrl}/stores/$selectedValue");
                    final responseStore = await http.get(urlStore);
                    final store = json.decode(responseStore.body);
                    final email = prefs.getString('email');
                    final urlOpen = Uri.parse("${Urls.baseUrl}/open");
                    var data = {
                      'user_email': email,
                      'store': store['id'],
                    };
                    var body = jsonEncode(data);
                    var headers = {'Content-Type': 'application/json'};

                    var responseOpen =
                        await http.post(urlOpen, headers: headers, body: body);

                    if (responseOpen.statusCode == 200) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Center(
                            child: Text('Comando enviado com sucesso!'),
                          ),
                        ),
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Center(
                            child: Text('Erro na abertura!'),
                          ),
                        ),
                      );
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
                            'Abrir loja',
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
            ),
            Container(
              alignment: Alignment.center,
              child: InkWell(
                onTap: () async {
                  SharedPreferences prefs =
                      await SharedPreferences.getInstance();
                  prefs.clear();
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(
                      builder: (context) => LoginScreen(),
                    ),
                  );
                },
                child: const Text(
                  'Sair',
                  style: TextStyle(
                    fontFamily: 'outfit',
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: Color.fromARGB(255, 237, 100, 90),
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
