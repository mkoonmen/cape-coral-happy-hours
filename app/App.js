// Cape Coral Happy Hours — one codebase for iPhone + Android (Expo / React Native).
// Data loads from the free GitHub-hosted feed (DATA_URL) so the list updates without an app update;
// falls back to the copy bundled in the app when offline.
import React, { useEffect, useMemo, useState } from 'react';
import { SafeAreaView, View, Text, TextInput, FlatList, Pressable, Linking, StyleSheet, StatusBar } from 'react-native';
import bundled from './restaurants.json';

// Replace OWNER with your GitHub username after the repo is created.
const DATA_URL = 'https://raw.githubusercontent.com/mkoonmen/cape-coral-happy-hours/main/data/restaurants.json';
const REPORT_URL = 'https://github.com/mkoonmen/cape-coral-happy-hours/issues/new';

const FILTERS = ['Happy hours', 'All', 'Not confirmed'];

export default function App() {
  const [data, setData] = useState(bundled);
  const [q, setQ] = useState('');
  const [filter, setFilter] = useState('Happy hours');

  useEffect(() => {
    fetch(DATA_URL, { cache: 'no-store' })
      .then(r => (r.ok ? r.json() : null))
      .then(j => { if (j && j.restaurants) setData(j); })
      .catch(() => {});
  }, []);

  const list = useMemo(() => data.restaurants
    .filter(r => filter === 'All' || (filter === 'Happy hours' ? r.happyHour.status === 'listed' : r.happyHour.status === 'unconfirmed'))
    .filter(r => (r.name + r.category + r.address + r.happyHour.deals).toLowerCase().includes(q.toLowerCase()))
    .sort((a, b) => (a.happyHour.status === 'listed' ? 0 : 1) - (b.happyHour.status === 'listed' ? 0 : 1) || a.name.localeCompare(b.name)),
    [data, q, filter]);

  const report = r => {
    const title = encodeURIComponent(`Happy hour update: ${r.name}`);
    const body = encodeURIComponent(`Restaurant: ${r.name}\nCurrent listing: ${r.happyHour.times || 'none'}\nCorrect days/times:\nDeals:\nSource (menu link/photo):`);
    Linking.openURL(`${REPORT_URL}?title=${title}&body=${body}&labels=update`);
  };

  return (
    <SafeAreaView style={s.wrap}>
      <StatusBar barStyle="light-content" />
      <Text style={s.h1}>Cape Coral Happy Hours</Text>
      <Text style={s.sub}>{data.restaurants.length} spots · updated {data.updated}</Text>
      <TextInput style={s.search} placeholder="Search restaurants, food, deals" placeholderTextColor="#7a8a99" value={q} onChangeText={setQ} />
      <View style={s.row}>
        {FILTERS.map(f => (
          <Pressable key={f} onPress={() => setFilter(f)} style={[s.chip, filter === f && s.chipOn]}>
            <Text style={[s.chipT, filter === f && s.chipTOn]}>{f}</Text>
          </Pressable>
        ))}
      </View>
      <FlatList
        data={list}
        keyExtractor={r => r.id}
        renderItem={({ item: r }) => (
          <View style={s.card}>
            <Text style={s.name}>{r.name}</Text>
            <Text style={s.meta}>{r.category} · {r.address}</Text>
            {r.happyHour.status === 'listed' ? (
              <>
                <Text style={s.time}>🍹 {r.happyHour.times}</Text>
                {!!r.happyHour.deals && <Text style={s.deals}>{r.happyHour.deals}</Text>}
              </>
            ) : <Text style={s.unk}>{r.happyHour.status === 'none_expected' ? 'Counter-service spot — no happy hour found' : 'Happy hour not confirmed yet — call to ask'}</Text>}
            {r.happyHour.status === 'listed' && <Text style={s.src}>Source: {r.happyHour.source}{r.happyHour.confidence === 'low' ? ' · older or less certain' : ''} · confirm with the restaurant</Text>}
            <View style={s.row}>
              <Pressable onPress={() => Linking.openURL(`https://maps.google.com/?q=${encodeURIComponent(r.name + ' ' + r.address)}`)}><Text style={s.link}>Directions</Text></Pressable>
              {!!r.phone && <Pressable onPress={() => Linking.openURL('tel:' + r.phone.replace(/\D/g, ''))}><Text style={s.link}>  Call</Text></Pressable>}
              <Pressable onPress={() => report(r)}><Text style={s.link}>  Suggest an update</Text></Pressable>
            </View>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const s = StyleSheet.create({
  wrap: { flex: 1, backgroundColor: '#0b1f2e', paddingHorizontal: 14 },
  h1: { color: '#fff', fontSize: 26, fontWeight: '800', marginTop: 10 },
  sub: { color: '#8fb3c9', marginBottom: 10 },
  search: { backgroundColor: '#13324a', color: '#fff', borderRadius: 10, padding: 12, fontSize: 16 },
  row: { flexDirection: 'row', flexWrap: 'wrap', marginTop: 8 },
  chip: { borderWidth: 1, borderColor: '#2b5877', borderRadius: 16, paddingVertical: 6, paddingHorizontal: 12, marginRight: 8, marginBottom: 6 },
  chipOn: { backgroundColor: '#ff8a3d', borderColor: '#ff8a3d' },
  chipT: { color: '#8fb3c9' }, chipTOn: { color: '#0b1f2e', fontWeight: '700' },
  card: { backgroundColor: '#112a3d', borderRadius: 12, padding: 14, marginVertical: 6 },
  name: { color: '#fff', fontSize: 18, fontWeight: '700' },
  meta: { color: '#8fb3c9', marginTop: 2 },
  time: { color: '#ffb37a', fontSize: 16, fontWeight: '700', marginTop: 8 },
  deals: { color: '#dfe9f0', marginTop: 4 },
  unk: { color: '#6f8496', fontStyle: 'italic', marginTop: 8 },
  src: { color: '#6f8496', fontSize: 12, marginTop: 6 },
  link: { color: '#4fc3f7', fontWeight: '600' },
});
