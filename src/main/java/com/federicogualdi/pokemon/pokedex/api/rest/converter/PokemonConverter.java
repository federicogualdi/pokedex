package com.federicogualdi.pokemon.pokedex.api.rest.converter;

import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokeApiPokemonFlavorTextEntriesDto;
import com.federicogualdi.pokemon.pokedex.messages.rest.dto.PokemonDto;

import javax.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class PokemonConverter {

    public PokemonDto fromPokeAPi(PokeApiPokemonDto pokemonPokeApi) {
        PokemonDto pokemonConverted = new PokemonDto();
        pokemonConverted.name = pokemonPokeApi.name;
        pokemonConverted.habitat = pokemonPokeApi.habitat.name;
        pokemonConverted.isLegendary = pokemonPokeApi.isLegendary;

        if (!pokemonPokeApi.flavorTextEntries.isEmpty()) {
            pokemonConverted.description = pokemonPokeApi.flavorTextEntries.stream().filter(PokeApiPokemonFlavorTextEntriesDto::isEnglish).findFirst().map(d -> d.flavorText.replaceAll("\\n", " ").replaceAll("\\f", " ")).orElse(null);
        }

        return pokemonConverted;
    }
}
