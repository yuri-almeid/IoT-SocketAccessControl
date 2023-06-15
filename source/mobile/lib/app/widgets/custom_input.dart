import 'package:flutter/material.dart';

InputDecoration customTextFieldDecoration(
    {String hintText = 'You have to put something here dumbass'}) {
  return InputDecoration(
    isDense: true,
    labelText: hintText,
    hintStyle: const TextStyle(
      color: Color(0xFF555454),
      fontFamily: 'outfit',
      fontWeight: FontWeight.w400,
      fontSize: 16,
    ),
    border: const OutlineInputBorder(
      borderRadius: BorderRadius.all(
        Radius.circular(60.0),
      ),
    ),
    focusedBorder: const OutlineInputBorder(
      borderSide: BorderSide(color: Colors.blue, width: 1.4),
      borderRadius: BorderRadius.all(
        Radius.circular(49.0),
      ),
    ),
    enabledBorder: const OutlineInputBorder(
      borderSide: BorderSide(color: Colors.grey, width: 0.7),
      borderRadius: BorderRadius.all(
        Radius.circular(49.0),
      ),
    ),
  );
}
