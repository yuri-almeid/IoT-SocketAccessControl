import 'package:flutter/material.dart';
import 'package:mobile/app/screens/splash.dart';
// import 'package:mobile/app/screens/test_page.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // home: const SplashScreen(),
      home: const SplashScreen(),
    );
  }
}
