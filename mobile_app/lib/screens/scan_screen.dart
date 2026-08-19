
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import 'dart:convert';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State&lt;ScanScreen&gt; createState() =&gt; _ScanScreenState();
}

class _ScanScreenState extends State&lt;ScanScreen&gt; {
  final _usernameController = TextEditingController();
  final _urlController = TextEditingController();
  bool _isScanning = false;
  bool _isAnalyzing = false;
  Map&lt;String, dynamic&gt;? _result;
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Profile')),
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          _buildUsernameTab(),
          _buildURLTab(),
          _buildQRTab(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.person_search),
            label: 'Username',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.link),
            label: 'URL',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.qr_code_scanner),
            label: 'QR Code',
          ),
        ],
      ),
    );
  }

  Widget _buildUsernameTab() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Enter Instagram Username',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _usernameController,
            decoration: const InputDecoration(
              labelText: '@username',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.alternate_email),
            ),
          ),
          const SizedBox(height: 24),
          _isAnalyzing
              ? const Center(child: CircularProgressIndicator())
              : ElevatedButton(
                  onPressed: () async {
                    setState(() {
                      _isAnalyzing = true;
                    });
                    final api = Provider.of&lt;ApiService&gt;(context, listen: false);
                    try {
                      final result =
                          await api.analyzeProfile(_usernameController.text);
                      setState(() {
                        _result = result;
                      });
                    } catch (e) {
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Error: $e')),
                        );
                      }
                    } finally {
                      setState(() {
                        _isAnalyzing = false;
                      });
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 50),
                  ),
                  child: const Text('Analyze Profile'),
                ),
          if (_result != null) _buildResult(),
        ],
      ),
    );
  }

  Widget _buildURLTab() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Enter Profile URL',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _urlController,
            decoration: const InputDecoration(
              labelText: 'https://instagram.com/...',
              border: OutlineInputBorder(),
              prefixIcon: Icon(Icons.link),
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 50),
            ),
            child: const Text('Scan URL'),
          ),
        ],
      ),
    );
  }

  Widget _buildQRTab() {
    return Column(
      children: [
        Expanded(
          child: _isScanning
              ? MobileScanner(
                  onDetect: (capture) {
                    final List&lt;Barcode&gt; barcodes = capture.barcodes;
                    for (final barcode in barcodes) {
                      if (barcode.rawValue != null &amp;&amp; mounted) {
                        setState(() {
                          _isScanning = false;
                        });
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                              content: Text('Scanned: ${barcode.rawValue}')),
                        );
                      }
                    }
                  },
                )
              : Center(
                  child: ElevatedButton.icon(
                    onPressed: () {
                      setState(() {
                        _isScanning = true;
                      });
                    },
                    icon: const Icon(Icons.qr_code_scanner),
                    label: const Text('Start Scanning'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(200, 50),
                    ),
                  ),
                ),
        ),
      ],
    );
  }

  Widget _buildResult() {
    return Card(
      margin: const EdgeInsets.only(top: 24),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Analysis Results',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            if (_result!['final_result'] != null)
              ListTile(
                title: Text(_result!['final_result']),
              ),
          ],
        ),
      ),
    );
  }
}
