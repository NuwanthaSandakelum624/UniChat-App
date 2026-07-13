import React, { useState } from 'react';
import { View, Button, Image, StyleSheet } from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';

const App = () => {
  const [imageUri, setImageUri] = useState(null);

  const openImagePicker = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
    };

    launchImageLibrary(options, (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.assets) {
        setImageUri(response.assets[0].uri);
      }
    });
  };

  return (
    <View style={styles.container}>
      {imageUri && (
        <Image source={{ uri: imageUri }} style={styles.image} />
      )}
      <Button title="පින්තූරයක් තෝරන්න" onPress={openImagePicker} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  image: { width: 300, height: 300, marginBottom: 20 },
});

export default App;
