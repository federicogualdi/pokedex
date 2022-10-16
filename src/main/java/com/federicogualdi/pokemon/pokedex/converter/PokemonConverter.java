package com.federicogualdi.pokemon.pokedex.converter;

import com.federicogualdi.pokemon.pokedex.rest.dto.PokeApiPokemonDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokeApiPokemonFlavorTextEntriesDto;
import com.federicogualdi.pokemon.pokedex.rest.dto.PokemonDto;
import com.federicogualdi.pokemon.pokedex.services.TranslatorService;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;

@ApplicationScoped
public class PokemonConverter {

    @Inject
    TranslatorService translatorService;

    public PokemonDto from(PokeApiPokemonDto pokemonPokeApi) {
        return new PokemonDto.Builder()
                .name(pokemonPokeApi.name)
                .description(pokemonPokeApi.flavorTextEntries.stream()
                        .filter(PokeApiPokemonFlavorTextEntriesDto::isEnglish).findFirst()
                        .map(d -> d.getFlavorText())
                        .orElse(null)
                )
                .habitat(pokemonPokeApi.getHabitatName())
                .isLegendary(pokemonPokeApi.isLegendary)
                .build();
    }

    public PokemonDto toYodaTranslation(PokemonDto pokemonDto) {
        return translatorService.applyYodaTranslation(pokemonDto);
    }

    public PokemonDto toShakespeareTranslation(PokemonDto pokemonDto) {
        return translatorService.applyShakespeareTranslation(pokemonDto);
    }

}
