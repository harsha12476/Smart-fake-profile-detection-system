
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService extends ChangeNotifier {
  static const String baseUrl = 'http://10.0.2.2:5001';

  Future&lt;bool&gt; login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      body: {'email': email, 'password': password},
    );
    if (response.statusCode == 200) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('loggedIn', true);
      return true;
    }
    return false;
  }

  Future&lt;bool&gt; isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('loggedIn') ?? false;
  }

  Future&lt;void&gt; logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('loggedIn');
  }

  Future&lt;Map&lt;String, dynamic&gt;&gt; analyzeProfile(String username) async {
    final response = await http.post(
      Uri.parse('$baseUrl/analyze-profile'),
      body: {'username': username},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to analyze profile');
    }
  }

  Future&lt;Map&lt;String, dynamic&gt;&gt; analyzeFakeFollowers(
    String username,
    int followers,
    int following,
    int avgLikes,
    int avgComments,
    int accountAgeDays,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/analyze-fake-followers'),
      body: {
        'username': username,
        'followers': followers.toString(),
        'following': following.toString(),
        'avg_likes': avgLikes.toString(),
        'avg_comments': avgComments.toString(),
        'account_age_days': accountAgeDays.toString(),
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to analyze fake followers');
    }
  }

  Future&lt;Map&lt;String, dynamic&gt;&gt; analyzeCybercrime(
    String username,
    String bio,
    String captions,
    String links,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/analyze-cybercrime'),
      body: {
        'username': username,
        'bio': bio,
        'captions': captions,
        'links': links,
      },
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to analyze cybercrime');
    }
  }
}
